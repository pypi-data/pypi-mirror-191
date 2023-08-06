# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
import inspect
from typing import cast
from typing import Any
from typing import Callable
from typing import Generator
from typing import TypeVar

from .aggregateroot import AggregateRoot
from .domainevent import DomainEvent
from .event import Event
from .eventsourcemetaclass import EventSourceMetaclass
from .eventsourcestate import EventSourceState


R = TypeVar('R')


class EventSource(AggregateRoot, metaclass=EventSourceMetaclass):
    __module__: str = 'ddd'
    __abstract__: bool = True
    __state__: EventSourceState

    def init_state( # type: ignore
        self,
        state: EventSourceState,
        params: Any
    ) -> None:
        super().init_state(state, params or state.initial)

    @staticmethod
    def publisher(
        func: Callable[..., Generator[DomainEvent, None, R]]
    ) -> Callable[..., R]:
        """Mark a function to return domain events."""
        if not inspect.isgeneratorfunction(func):
            raise TypeError("Domain event publishers must be generators")

        @functools.wraps(func)
        def f(self: EventSource, *args: Any, **kwargs: Any) -> R:
            generator = func(self, *args, **kwargs)
            retval = None
            while True:
                try:
                    event = generator.send(None)
                    if not isinstance(event, DomainEvent): # type: ignore
                        raise TypeError(
                            "Domain event publishers must generate domain "
                            "events."
                        )
                    self._publish(event)
                except StopIteration as result:
                    retval = result.value
                    break
            return cast(R, retval)

        return f

    def replay(self, event: Event) -> None:
        """Replay the event without modifying the state."""
        domain = self.__meta__.parse_event(event.data)
        domain.apply(self)

    def _publish(self, event: DomainEvent) -> None:
        self.__state__.apply(self, event)