# Copyright (C) 2022-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from ..aggregatemeta import AggregateMeta
from ..aggregateroot import AggregateRoot
from ..aggregatestate import AggregateState


class IRepository:
    __module__: str = 'ddd.types'
    meta: AggregateMeta
    model: type[AggregateRoot]

    async def allocate(
        self,
        state: AggregateState,
        insert: bool
    ) -> int | str:
        """Allocate a new identifier for the entity."""
        raise NotImplementedError("Subclasses must override this method.")

    async def flush(
        self,
        new: AggregateState,
        insert: bool
    ) -> None:
        """Performs the actual write of the domain objects' state to
        the storage backend.

        Subclasses must override this method.

        Args:
            new (:class:`AggregateState`): the new state of the aggregate.
            insert (bool): indicates if the object is new i.e. an insert.

        Returns:
            None
        """
        raise NotImplementedError("Subclasses must override this method.")

    async def restore(self, id: int | str | None) -> AggregateState | None:
        """Restore the state of an aggregate from the storage backend."""
        raise NotImplementedError("Subclasses must override this method.")