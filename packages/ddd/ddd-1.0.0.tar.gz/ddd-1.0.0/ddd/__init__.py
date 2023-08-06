# pylint: skip-file
# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .aggregatemeta import AggregateMeta
from .aggregateroot import AggregateRoot
from .aggregatestate import AggregateState
from .aggregatestatedescriptor import AggregateStateDescriptor
from .domainevent import DomainEvent
from .entity import Entity
from .eventrepository import EventRepository
from .eventsource import EventSource
from .factory import Factory
from .repository import Repository
from .memoryeventrepository import MemoryEventRepository
from .memoryrepository import MemoryRepository
from . import exc
from . import utils


__all__: list[str] = [
    'exc',
    'publisher',
    'utils',
    'AggregateMeta',
    'AggregateRoot',
    'AggregateState',
    'AggregateStateDescriptor',
    'DomainEvent',
    'Entity',
    'EventRepository',
    'EventSource',
    'Factory',
    'MemoryEventRepository',
    'MemoryRepository',
    'Repository',
]

publisher = EventSource.publisher