# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
from typing import Any
from typing import TypeVar

from .aggregatestate import AggregateState
from .predicate import Predicate
from .predicateoperator import PredicateOperator
from .types import ICursor
from .types import IRepository


T = TypeVar('T')


class MemoryCursor(ICursor[T]):

    def __init__(self, objects: list[Any]):
        self.objects = objects

    def one(self) -> None | T:
        if len(self.objects) > 1:
            raise Exception("Expected one object.")
        return self.objects[0] if self.objects else None


class MemoryRepository(IRepository):
    __module__: str = 'ddd'
    objects: dict[int | str, dict[str, Any]] = {}

    def __new__(cls, *args: Any, **kwargs: Any):
        self = super().__new__(cls, *args, **kwargs)
        self.objects = {}
        return self

    async def allocate(self, state: AggregateState, insert: bool) -> int | str:
        """Allocate a new identifier for the entity."""
        return state.id or bytes.hex(os.urandom(16))

    async def flush(self, new: AggregateState, insert: bool) -> None:
        assert (insert and new.id not in self.objects) or not insert # nosec
        assert new.id is not None
        self.objects[new.id] = new.dict(exclude={'id'})

    async def restore(self, id: int | str | None) -> AggregateState | None:
        if id in self.objects:
            return self.meta.model.parse_obj({
                **self.objects[id],
                'id': id
            })

    def filter_by_predicate(
        self,
        *predicates: Predicate,
        limit: int = 100,
        token: str | None = None
    ) -> ICursor[Any]:
        objects: list[Any] = []
        for id, obj in self.objects.items():
            matching: list[bool] = []
            for predicate in predicates:
                found = False
                if not predicate.can_apply(self.meta):
                    continue
                if predicate.operator == PredicateOperator.eq:
                    if obj['spec'].get(predicate.name) == predicate.value:
                        found = True
                else:
                    raise NotImplementedError(predicate)
                matching.append(found)
            if all(matching):
                objects.append(self._restore(id, obj))
        return MemoryCursor(objects)

    def _restore(self, id: int | str, obj: dict[str, Any]):
        return self.meta.model.parse_obj({
            **obj,
            'id': id
        })