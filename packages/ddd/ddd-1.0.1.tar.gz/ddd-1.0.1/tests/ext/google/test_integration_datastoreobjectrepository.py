# Copyright (C) 2022-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pytest
from google.cloud.datastore import Client

from ddd.test import IFulfillmentRepository
from ddd.test import FulfillmentFactory
from ddd.test.repository import *
from ddd.ext.google import DatastoreObjectRepository


@pytest.fixture
def factory() -> FulfillmentFactory:
    return FulfillmentFactory()


@pytest.fixture
def repo(
    client: Client
) -> DatastoreObjectRepository:
    return DatastoreFulfillmentRepository(client)


class DatastoreFulfillmentRepository(IFulfillmentRepository, DatastoreObjectRepository):
    pass