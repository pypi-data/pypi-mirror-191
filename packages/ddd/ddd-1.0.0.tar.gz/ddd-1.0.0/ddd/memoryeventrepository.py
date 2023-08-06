# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
from collections import defaultdict
from typing import Any
from typing import AsyncGenerator

from .event import Event
from .eventsourcestate import EventSourceState
from .memoryrepository import MemoryRepository


class MemoryEventRepository(MemoryRepository):
    __module__: str = 'ddd'
    _events: dict[int | str, Event] = {}
    _objects: dict[int | str, dict[str, Any]] = {}

    def __new__(cls, *args: Any, **kwargs: Any):
        self = super().__new__(cls, *args, **kwargs)
        self._events = {}
        return self

    async def allocate_event(self, event: Event) -> int | str:
        """Allocate a new identifier for the event."""
        return event.id or bytes.hex(os.urandom(16))

    async def events(self, id: int | str) -> AsyncGenerator[Event, None]:
        for event in self._events.values():
            if event.aggregate_id != id:
                continue
            yield event

    async def flush_event(
        self,
        state: EventSourceState,
        event: Event
    ) -> None:
        assert state.id is not None
        assert event.id is not None
        self._events[event.id] = event