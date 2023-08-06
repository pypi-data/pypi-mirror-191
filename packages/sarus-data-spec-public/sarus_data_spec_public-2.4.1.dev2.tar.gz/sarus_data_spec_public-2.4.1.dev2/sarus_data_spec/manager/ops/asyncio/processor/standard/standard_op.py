import hashlib
import typing as t

import numpy as np
import pyarrow as pa

from sarus_data_spec.dataset import Dataset
from sarus_data_spec.manager.ops.asyncio.base import (
    BaseDatasetOp,
    BaseScalarOp,
)
from sarus_data_spec.scalar import Scalar
import sarus_data_spec.typing as st


class StandardDatasetOp(BaseDatasetOp):
    """Object that executes first routing among ops between
    transformed/source and processor
    """

    def pep_token(
        self, public_context: t.List[str], privacy_limit: st.PrivacyLimit
    ) -> t.Optional[str]:
        """By default we implement that the transform inherits the PEP status
        but changes the PEP token."""
        parent_token = self.parent().pep_token()
        if parent_token is None:
            return None

        transform = self.dataset.transform()
        h = hashlib.md5()
        h.update(parent_token.encode("ascii"))
        h.update(transform.protobuf().SerializeToString())

        return h.hexdigest()

    def parents(self) -> t.List[st.DataSpec]:
        return parents(self.dataset)

    def parent(self, kind: str = 'dataset') -> t.Union[st.Dataset, st.Scalar]:
        return parent(self.dataset, kind=kind)

    async def parent_to_arrow(
        self, batch_size: int = 10000
    ) -> t.AsyncIterator[pa.RecordBatch]:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        parent_iterator = await parent.manager().async_to_arrow(
            parent, batch_size=batch_size
        )
        return await self.decoupled_async_iter(parent_iterator)

    async def parent_schema(self) -> st.Schema:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        return await parent.manager().async_schema(parent)

    async def parent_value(self) -> t.Any:
        parent = self.parent(kind='scalar')
        assert isinstance(parent, Scalar)
        return await parent.manager().async_value(parent)

    async def parent_size(self) -> st.Size:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        return await parent.manager().async_size(parent)

    async def parent_bounds(self) -> st.Bounds:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        return await parent.manager().async_bounds(parent)

    async def parent_marginals(self) -> st.Marginals:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        return await parent.manager().async_marginals(parent)

    async def ensure_batch_correct(
        self,
        async_iterator: t.AsyncIterator[pa.RecordBatch],
        func_to_apply: t.Callable,
        batch_size: int,
    ) -> t.AsyncIterator[pa.RecordBatch]:
        """Method that executes func_to_apply on each batch
        of the async_iterator but rather than directly returning
        the result, it accumulates them and returns them progressively
        so that each new batch has batch_size."""

        global_array = None
        async for batch in async_iterator:
            new_array = await func_to_apply(batch)
            if len(new_array) == batch_size and global_array is None:
                yield pa.RecordBatch.from_struct_array(new_array)
            elif global_array is not None:
                global_array = pa.concat_arrays([global_array, new_array])
                if len(global_array) < batch_size:
                    continue
                else:
                    # here cannot use array.slice because there
                    # is a bug in the columns being copied
                    # when we switch to record batch
                    yield pa.RecordBatch.from_struct_array(
                        global_array.take(
                            np.linspace(
                                0, batch_size - 1, batch_size, dtype=int
                            )
                        )
                    )
                    global_array = global_array.take(
                        np.linspace(
                            batch_size,
                            len(global_array) - 1,
                            len(global_array) - batch_size,
                            dtype=int,
                        )
                    )

            else:
                # initialize global_array
                global_array = new_array
                continue
        # handle remaining array: split it in

        if global_array is not None and len(global_array) > 0:
            while len(global_array) > 0:
                min_val = min(batch_size, len(global_array))
                indices = np.linspace(
                    0, len(global_array) - 1, len(global_array), dtype=int
                )
                yield pa.RecordBatch.from_struct_array(
                    global_array.take(indices[:min_val])
                )
                global_array = global_array.take(indices[min_val:])


class StandardScalarOp(BaseScalarOp):
    def parent(self, kind: str = 'dataset') -> st.DataSpec:
        return parent(self.scalar, kind=kind)

    def parents(self) -> t.List[st.DataSpec]:
        return parents(self.scalar)

    async def parent_to_arrow(
        self, batch_size: int = 10000
    ) -> t.AsyncIterator[pa.RecordBatch]:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        parent_iterator = await parent.manager().async_to_arrow(
            parent, batch_size=batch_size
        )
        return await self.decoupled_async_iter(parent_iterator)

    async def parent_schema(self) -> st.Schema:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        return await parent.manager().async_schema(parent)

    async def parent_value(self) -> t.Any:
        parent = self.parent(kind='scalar')
        assert isinstance(parent, Scalar)
        return await parent.manager().async_value(parent)


def parent(dataspec: st.DataSpec, kind: str) -> t.Union[st.Dataset, st.Scalar]:
    pars = parents(dataspec)
    if kind == 'dataset':
        parent: t.Union[t.List[Scalar], t.List[Dataset]] = [
            element for element in pars if isinstance(element, Dataset)
        ]
    else:
        parent = [element for element in pars if isinstance(element, Scalar)]
    assert len(parent) == 1
    return parent[0]


def parents(dataspec: st.DataSpec) -> t.List[st.DataSpec]:
    parents_args, parents_kwargs = dataspec.parents()
    parents_args.extend(parents_kwargs.values())
    return parents_args
