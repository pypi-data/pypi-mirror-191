# Copyright (C) 2022-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pytest

import ddd
from ddd.test import EventSourcedFulfillment
from ddd.test import EventSourcedFulfillmentFactory
from ddd.test import EventSourcedFulfillmentRepository
from ddd.test.repository import *


@pytest.fixture
def factory() -> EventSourcedFulfillmentFactory:
    return EventSourcedFulfillmentFactory()


@pytest.fixture
def repo() -> EventSourcedFulfillmentRepository:
    return EventSourcedFulfillmentRepository()


def test_get(
    factory: EventSourcedFulfillmentFactory
) -> None:
    obj = factory.new(order_id=1)
    assert obj.order_id == 1


def test_get_class() -> None:
    assert isinstance(EventSourcedFulfillment.order_id, ddd.AggregateStateDescriptor)


def test_set(
    factory: EventSourcedFulfillmentFactory
) -> None:
    obj = factory.new(order_id=1)
    obj.order_id = 2
    assert obj.order_id == 2