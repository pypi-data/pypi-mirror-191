# Copyright (C) 2022-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Declares :class:`Repository`."""
import contextlib
import functools
from typing import Any
from typing import Awaitable
from typing import Generic
from typing import TypeVar

from .aggregateroot import AggregateRoot
from .aggregatemeta import AggregateMeta
from .aggregatestate import AggregateState
from .exc import StaleDomainObject
from .filterresult import FilterResult
from .predicate import PaginationToken
from .predicate import Predicate
from .repositorymetaclass import RepositoryMetaclass
from .types import ICursor
from .types import IRepository


T = TypeVar('T', bound=AggregateRoot)


class Repository(IRepository, Generic[T], metaclass=RepositoryMetaclass):
    """Provide a base class implementation for DDD repositories."""
    __module__: str = 'ddd'
    __abstract__: bool = True
    meta: AggregateMeta
    model: type[T]

    def increment(self, state: AggregateState) -> None:
        """Increment the version of the state."""
        state.increment()

    def filter(self,
        p: bool | str | PaginationToken | Predicate,
        *args: Predicate,
        limit: int = 100,
        token: str | None = None
    ) -> Awaitable[FilterResult[T]]:
        """Filter objects based on the predicate."""
        if isinstance(p, str):
            p = PaginationToken(p)
        return FilterResult(self._filter_by_predicate(p, *args, limit=limit, token=token))

    async def find(self, attname: str | Predicate | bool, *args: Any) -> None | T:
        # Note that this function does not accept a boolean, but it is needed
        # to silence the type checker.
        cursor = await self._find(attname, *args)
        state = cursor.one()
        if state is not None:
            return self.reconstruct_model(state)

    @functools.singledispatchmethod
    def _find(self, attname: str | Predicate, *args: Any) -> ICursor[T]:
        raise NotImplementedError

    @_find.register
    def _filter_by_attribute(self, attname: str, value: Any) -> ICursor[T]:
        return self.filter_by_predicate(getattr(self.model, attname)==value)

    @_find.register
    def _filter_by_predicate(
        self,
        predicate: Predicate,
        *args: Predicate,
        limit: int = 100,
        token: str | None = None
    ) -> ICursor[T]:
        return self.filter_by_predicate(predicate, *args, limit=limit, token=token)

    async def get(self, id: int | str | None) -> None | T:
        """Restore a domain object from the storage backend using
        its identifier.
        """
        if id is None:
            return None
        state = await self.restore(id)
        return self.reconstruct_model(state) if state else None

    async def persist(self, instance: T) -> T:
        """Persist an aggregate to the data storage platform."""
        await self.persist_state(instance.__state__)
        return instance

    async def persist_state(
        self,
        new: AggregateState
    ) -> None:
        """Use the domain models' metadata and state to tranform
        the object to the storage format and persist it to the
        storage backend.
        """
        if not new.is_dirty(): # pragma: no cover
            return
        async with self.transaction():
            old = await self.restore(new.id)
            insert = old is None
            if old is not None:
                if new.version != old.version:
                    raise StaleDomainObject(f"{self.meta.name} is stale.")
            self.increment(new)
            if not new.id:
                assert old is None
                new.id = await self.allocate(new, insert)
            await self.begin_flush(new, old, insert)

    def reconstruct_model(
        self,
        state: Any
    ) -> None | T:
        return self.model(state)

    @contextlib.asynccontextmanager
    async def transaction(self):
        yield

    async def begin_flush(
        self,
        new: Any,
        old: Any,
        insert: bool
    ) -> None:
        return await self.flush(new, insert)