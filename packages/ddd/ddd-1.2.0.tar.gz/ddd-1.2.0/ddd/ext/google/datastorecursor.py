# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Generic
from typing import TypeVar

from google.cloud.datastore import Entity

from ddd import AggregateMeta
from ddd import AggregateState
from ddd.types import ICursor
from .datastorequery import DatastoreQuery
from .runner import Runner


T = TypeVar('T', bound=AggregateState)


class DatastoreCursor(ICursor[Any], Generic[T], Runner):
    meta: AggregateMeta
    query: DatastoreQuery
    _objects: list[T]

    def __init__(
        self,
        meta: AggregateMeta,
        query: DatastoreQuery
    ):
        self.meta = meta
        self.query = query
        self._objects = []
        self._token = None

    def add_filter(self, attr: str, operator: str, value: Any) -> None:
        self.query.add_filter(attr, operator, value) # type: ignore

    def all(self) -> list[T]:
        return self._objects

    def get_pagination_token(self) -> str | None:
        return self._token

    def one(self) -> Any | None:
        """Fetch one object from the datastore. Raises an error if there is more
        than one object.
        """
        if len(self._objects) > 1:
            raise self.MultipleObjectsReturned
        return self._objects[0] if self._objects else None

    async def fetch(self) -> 'ICursor[T]':
        cursor = await self.run_in_executor(self.query.fetch)
        for entity in cursor: # type: ignore
            self._objects.append(self._restore(entity))
            if cursor.next_page_token:
                self._token = bytes.hex(cursor.next_page_token)
        return self

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

    async def __anext__(self):
        try:
            return self._objects.pop(0)
        except IndexError:
            raise StopAsyncIteration