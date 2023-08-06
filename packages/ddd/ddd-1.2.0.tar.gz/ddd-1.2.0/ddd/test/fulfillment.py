# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import ddd

from .fulfillmentitem import FulfillmentItem
from .fulfillmentstatus import FulfillmentStatus


class Fulfillment(ddd.AggregateRoot):
    __module__: str = 'ddd.test'
    items: list[FulfillmentItem] = []
    order_id: int
    status: FulfillmentStatus = FulfillmentStatus.detected

    def add_item(self, line_id: int, sku: str, quantity: int) -> None:
        if self.status != FulfillmentStatus.detected:
            raise ValueError("Can not add any more items.")
        self.items.append(
            FulfillmentItem(line_id=line_id, sku=sku, quantity=quantity)
        )

    def accept(self) -> None:
        self.status = FulfillmentStatus.accepted

    def is_accepted(self) -> bool:
        return self.status in {
            FulfillmentStatus.accepted
        }

    def reject(self) -> None:
        self.status = FulfillmentStatus.rejected