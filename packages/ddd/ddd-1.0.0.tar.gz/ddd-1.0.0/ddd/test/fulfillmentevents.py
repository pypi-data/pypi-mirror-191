# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
from typing import TYPE_CHECKING

import pydantic

import ddd
if TYPE_CHECKING:
    from .eventsourcedfulfillment import EventSourcedFulfillment

from .fulfillmentstatus import FulfillmentStatus



class OrderDetected(ddd.DomainEvent):

    def apply(self, obj: 'EventSourcedFulfillment'):
        pass


class FulfillmentAccepted(ddd.DomainEvent):
    timestamp: datetime.datetime = pydantic.Field(
        default_factory=datetime.datetime.utcnow
    )

    def apply(self, obj: 'EventSourcedFulfillment') -> None:
        obj.status = FulfillmentStatus.accepted


class FulfillmentRejected(ddd.DomainEvent):
    timestamp: datetime.datetime = pydantic.Field(
        default_factory=datetime.datetime.utcnow
    )

    def apply(self, obj: 'EventSourcedFulfillment') -> None:
        obj.status = FulfillmentStatus.rejected


class FulfillmentRequested(ddd.DomainEvent):
    requested: datetime.datetime
    message: str | None = None

    def apply(self, obj: 'EventSourcedFulfillment'):
        obj.requested = self.requested
        obj.message = self.message