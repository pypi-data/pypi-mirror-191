# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import TypeVar

from google.cloud.datastore import Entity
from google.cloud.datastore import Query

from ddd import AggregateMeta
from ddd import AggregateState
from .runner import Runner


T = TypeVar('T', bound=AggregateState)


class DatastoreCursor(Runner):
    meta: AggregateMeta
    query: Query

    def __init__(self, meta: AggregateMeta, query: Query):
        self.meta = meta
        self.query = query

    def add_filter(self, attr: str, operator: str, value: Any) -> None:
        self.query.add_filter(attr, operator, value) # type: ignore

    async def one(self) -> Any | None:
        """Fetch one object from the datastore. Raises an error if there is more
        than one object.
        """
        entity: Entity | None = None
        for row in await self.run_in_executor(self.query.fetch): # type: ignore
            if entity is not None:
                raise Exception("Expected one object.")
            entity = row
        return self._restore(entity)

    def _restore(self, entity: dict[str, Any] | Entity | None) -> Any:
        if entity is None:
            return None
        if isinstance(entity, Entity):
            key = entity.key # type: ignore
            entity = dict(entity)
        return self.meta.model.parse_obj({
            **entity,
            'id': key.id # type: ignore
        })