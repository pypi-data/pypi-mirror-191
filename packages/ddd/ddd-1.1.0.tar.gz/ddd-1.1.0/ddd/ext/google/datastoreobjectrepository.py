# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
from typing import Any
from typing import TypeVar

from google.cloud.datastore import Client
from google.cloud.datastore import Entity
from google.cloud.datastore import Key
from google.cloud.datastore import Query

from ddd import AggregateState
from ddd.types import IRepository
from .datastorecursor import DatastoreCursor
from .runner import Runner


T = TypeVar('T')


class DatastoreObjectRepository(IRepository, Runner):
    __module__: str = 'ddd.ext.google'
    client: Client

    def __init__(
        self,
        client: Client
    ):
        self.client = client

    async def allocate(
        self,
        state: AggregateState,
        insert: bool
    ) -> int:
        base = self.storage_key(self.meta.name)
        key, *_ = await self.run_in_executor(
            functools.partial( # type: ignore
                self.client.allocate_ids, # type: ignore
                incomplete_key=base,
                num_ids=1
            )
        )
        return key.id

    async def filter_by_attribute(self, attname: str, value: Any) -> None | Any:
        return await self.query_by_attribute(attname, '=', value).one()

    async def flush(self, new: AggregateState, insert: bool) -> None:
        assert isinstance(new.id, int) # nosec
        entity = Entity(key=self.storage_key(id=new.id))
        entity.update(new.dict(exclude={'id'})) # type: ignore
        await self.put(entity)

    async def get_entity_by_id(
        self,
        entity_id: int,
        kind: str | None = None,
        parent: Key | None = None
    ) -> Entity | None:
        return await self.run_in_executor(
            functools.partial(
                self.client.get, # type: ignore
                key=self.storage_key(
                    kind or self.meta.name,
                    id=entity_id,
                    parent=parent
                )
            )
        )

    async def put(self, entity: Entity) -> Entity:
        await self.run_in_executor(self.client.put, entity) # type: ignore
        assert (entity.key.id or entity.key.name) is not None # type: ignore # nosec
        return entity

    async def restore(self, id: int | str | None) -> AggregateState | None:
        assert isinstance(id, int) or id is None # nosec
        obj = None
        if id is not None:
            entity = await self.get_entity_by_id(id)
            if entity is not None:
                obj = self.meta.model.parse_obj({
                    **entity,
                    'id': id
                })
        return obj

    def storage_key(
        self,
        kind: str | None = None,
        id: int | None = None,
        parent: Key | None = None
    ) -> Key:
        kind = kind or self.meta.name
        return (
            self.client.key(kind, id, parent=parent) # type: ignore
            if id is not None
            else self.client.key(kind, parent=parent) # type: ignore
        )

    def query(self, kind: str | None = None, ancestor: Key | None = None) -> Query:
        return self.client.query(kind=kind or self.meta.name, ancestor=ancestor) # type: ignore

    def query_by_attribute(
        self,
        attr: str,
        operator: str,
        value: str
    ) -> DatastoreCursor:
        query = self.query()
        query.add_filter(attr, operator, value) # type: ignore
        return DatastoreCursor(self.meta, query)