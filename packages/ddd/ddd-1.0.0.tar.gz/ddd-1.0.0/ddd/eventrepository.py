# Copyright (C) 2022-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Generic
from typing import TypeVar

from .aggregatestate import AggregateState
from .event import Event
from .eventsource import EventSource
from .eventsourcestate import EventSourceState
from .exc import StaleDomainObject
from .repository import Repository


T = TypeVar('T', bound=EventSource)


class EventRepository(Repository[T], Generic[T]):
    __abstract__: bool = True

    def increment(self, state: AggregateState) -> None:
        # Skip incrementing of the state because that is handled
        # while persisting events.
        pass

    async def begin_flush(
        self,
        new: EventSourceState,
        old: EventSourceState | None,
        insert: bool
    ) -> None:
        # Here we persist the events before flushing the domain
        # entity.
        pending = new.pending()
        for n, event in enumerate(pending):
            if n == 0 and old is not None:
                # The first event must match the version of
                # an existing object plus one.
                if (old.version + 1) != event.version:
                    raise StaleDomainObject
            await self.persist_event(new, event)

        if not pending:
            new.increment()

        return await super().begin_flush(new, old, insert)

    async def get(self, id: int | str | None) -> None | T:
        """Restore a domain object from the storage backend using
        its identifier.
        """
        obj = await super().get(id)
        if obj is not None:
            await self.replay(obj)
            return obj

    async def persist_event(
        self,
        state: EventSourceState,
        event: Event,
        previous: Event | None = None
    ) -> None:
        """Persist the event. Allocate an identifier and compare it to
        any existing object.
        """
        assert state.id is not None
        state.version = event.version
        event.aggregate_id = state.id
        event.id = await self.allocate_event(event)
        await self.flush_event(state, event)

    async def replay(self, obj: T) -> None:
        """Apply events to the object without modifying the metadata."""
        assert obj.__state__.id is not None
        async for event in self.events(obj.__state__.id):
            obj.replay(event)