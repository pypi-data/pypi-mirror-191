# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from .aggregatemeta import AggregateMeta
from .aggregatestate import AggregateState


class AggregateStateDescriptor:
    """Represents a state property of an :class:`AggregateRoot`."""
    __module__: str = 'ddd'
    dirty: bool = False
    name: str

    def __init__(
        self,
        name: str
    ):
        self.name = name

    def get(
        self,
        cls: type[Any],
        meta: AggregateMeta,
        state: AggregateState
    ) -> Any:
        return getattr(state.spec, self.name)

    def set(
        self,
        value: Any,
        meta: AggregateMeta,
        state: AggregateState
    ) -> Any:
        state.set(self.name, value)

    def __get__(
        self,
        obj: tuple[AggregateMeta, AggregateState] | None,
        cls: type[Any]
    ) -> Any:
        if obj is None:
            return self
        return self.get(cls, *obj)

    def __set__(
        self,
        obj: tuple[AggregateMeta, AggregateState],
        value: Any
    ) -> Any:
        return self.set(value, *obj) # type: ignore