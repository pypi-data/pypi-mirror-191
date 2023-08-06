# Copyright (C) 2022-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import pydantic

from .aggregatestate import AggregateState
from .domainevent import DomainEvent
from .event import Event


class EventSourceState(AggregateState):
    #: The current version of the aggregate based on the events published
    #: during its current lifecycle.
    events: list[Event] = []
    initial: dict[str, Any] = {}
    lifecycle: int

    @pydantic.root_validator(pre=True)
    def preprocess(cls, values: dict[str, Any]) -> dict[str, Any]:
        values.setdefault('lifecycle', values.get('version') or 0)
        return values

    def add(
        self,
        data: dict[str, Any]
    ) -> Event:
        event = Event(
            aggregate_id=self.id,
            data=data,
            version=self.lifecycle + 1
        )
        if self.events:
            if self.events[-1].version != event.version -1:
                raise ValueError('Version mismatch.')
        self.events.append(event)
        self.lifecycle = event.version
        return event

    def apply(self, obj: Any, event: DomainEvent) -> None:
        self.add(event.dict())
        try:
            event.apply(obj)
        except Exception:
            self.revert()
            raise

    def init(self, **kwargs: Any) -> None:
        # Retain the initial values so the object can be reconstructed,
        # since the constructor arguments are not represented by events.
        super().init(**kwargs)
        if self.version == 0:
            self.initial = self.spec.dict()

    def is_dirty(self) -> bool:
        """Return a boolean indicating if the state is dirty."""
        return bool(self.pending()) or not self.id

    def latest(self) -> Event | None:
        """Return the latest event."""
        return self.events[-1] if self.events else None

    def pending(self) -> list[Event]:
        """Return all events that are not saved to the datastore."""
        return [x for x in self.events if x.id is None]

    def revert(self):
        """Revert the latest event."""
        event = self.events.pop()
        if self.events:
            self.lifecycle = self.events[-1].version
        assert self.lifecycle == (event.version - 1)

    def create_snapshot(self, **kwargs: Any) -> dict[str, Any]:
        assert self.spec is not None # nosec
        return {
            'event': self.version,
            'data': self.spec.dict()
        }

    def dict(self, **kwargs: Any) -> dict[str, Any]:
        exclude = kwargs.setdefault('exclude', set())
        exclude.add('events')
        exclude.add('lifecycle')
        exclude.add('spec')
        return super().dict(**kwargs)