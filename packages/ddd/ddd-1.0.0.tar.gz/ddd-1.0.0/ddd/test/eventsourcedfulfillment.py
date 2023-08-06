# type: ignore
# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime

import ddd
from .fulfillmentevents import FulfillmentAccepted
from .fulfillmentevents import FulfillmentRejected
from .fulfillmentevents import FulfillmentRequested
from .fulfillmentitem import FulfillmentItem
from .fulfillmentstatus import FulfillmentStatus


class EventSourcedFulfillment(ddd.EventSource):
    __module__: str = 'ddd.test'
    items: list[FulfillmentItem] = []
    message: str | None = None
    order_id: int
    requested: datetime.datetime | None = None
    status: FulfillmentStatus = FulfillmentStatus.detected

    @ddd.publisher
    def request(
        self,
        requested: datetime.datetime,
        message: str | None = None
    ):
        """Request the fulfillment of the specified order."""
        yield FulfillmentRequested(message=message, requested=requested)

    @ddd.publisher
    def accept(self) -> None:
        """Accpet the fulfillment."""
        yield FulfillmentAccepted()

    @ddd.publisher
    def reject(self) -> None:
        """Reject the fulfillment."""
        yield FulfillmentRejected()

    def is_accepted(self) -> bool:
        return self.status in {
            FulfillmentStatus.accepted
        }