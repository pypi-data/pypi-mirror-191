# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Declares :class:`AggregateRoot`."""
from typing import Any

from .aggregaterootmetaclass import AggregateRootMetaclass
from .aggregatemeta import AggregateMeta
from .aggregatestate import AggregateState


class AggregateRoot(metaclass=AggregateRootMetaclass):
    """Encapsulates a domain model and represents an atomic unit through which
    data changes are made. An aggregate is a collection of one or more related
    entities (and possibly value objects). Each aggregate has a single root
    entity, referred to as the aggregate root. The aggregate root is
    responsible for controlling access to all of the members of its
    aggregate.
    """
    __module__: str = 'ddd'
    __abstract__: bool = True
    __meta__: AggregateMeta
    __state__: AggregateState

    def __init__(
        self,
        state: AggregateState | None,
        /,
        **kwargs: Any
    ):
        state = state or self.__meta__.model()
        if state.spec is None:
            state.init(**kwargs)
        self.__state__ = state

    def __iter__(self) -> tuple[AggregateMeta, AggregateState]:
        return iter((self.__meta__, self.__state__)) # type: ignore
