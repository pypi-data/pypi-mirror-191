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

from .aggregatestate import AggregateState
from .types import IRepository


class MemoryRepository(IRepository):
    __module__: str = 'ddd'
    _objects: dict[int | str, dict[str, Any]] = {}

    def __new__(cls, *args: Any, **kwargs: Any):
        self = super().__new__(cls, *args, **kwargs)
        self._objects = {}
        return self

    async def allocate(self, state: AggregateState, insert: bool) -> int | str:
        """Allocate a new identifier for the entity."""
        return state.id or bytes.hex(os.urandom(16))

    async def flush(self, new: AggregateState, insert: bool) -> None:
        assert (insert and new.id not in self._objects) or not insert # nosec
        assert new.id is not None
        self._objects[new.id] = new.dict(exclude={'id'})

    async def restore(self, id: int | str | None) -> AggregateState | None:
        if id in self._objects:
            return self.meta.model.parse_obj({
                **self._objects[id],
                'id': id
            })