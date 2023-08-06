# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pytest

from ..exc import StaleDomainObject
from .fulfillmentfactory import FulfillmentFactory
from .fulfillmentrepository import FulfillmentRepository


__all__: list[str] = [
    'test_repo_new_persist_get',
    'test_repo_persist_updates_version',
    'test_repo_concurrent_write_is_rejected',
    'test_repo_get_with_no_id_returns_none',
    'test_repo_persists_state',
    'test_repo_persists_state_on_existing_object',
]


@pytest.mark.asyncio
async def test_repo_new_persist_get(
    factory: FulfillmentFactory,
    repo: FulfillmentRepository
) -> None:
    old = factory.new(order_id=1)
    await repo.persist(old)
    new = await repo.get(old.__state__.id)
    assert new is not None
    assert old.order_id == new.order_id


@pytest.mark.asyncio
async def test_repo_persist_updates_version(
    factory: FulfillmentFactory,
    repo: FulfillmentRepository
) -> None:
    obj = factory.new(order_id=1)
    await repo.persist(obj)
    assert obj.__state__.version == 1, obj.__state__.version


@pytest.mark.asyncio
async def test_repo_persists_state(
    factory: FulfillmentFactory,
    repo: FulfillmentRepository
) -> None:
    obj = factory.new(order_id=1)
    obj.accept()
    await repo.persist(obj)
    stored = await repo.get(obj.__state__.id)
    assert stored is not None
    assert stored.is_accepted()


@pytest.mark.asyncio
async def test_repo_does_not_persist_unmodified(
    factory: FulfillmentFactory,
    repo: FulfillmentRepository
):
    obj = factory.new(order_id=1)
    obj.accept()
    await repo.persist(obj)
    stored = await repo.get(obj.__state__.id)
    assert stored is not None
    stored.accept()
    assert not stored.__state__.is_dirty()
    await repo.persist(stored)


@pytest.mark.asyncio
async def test_repo_persists_state_on_existing_object(
    factory: FulfillmentFactory,
    repo: FulfillmentRepository
) -> None:
    obj = factory.new(order_id=1)
    await repo.persist(obj)
    assert obj.__state__.version == 1

    stored = await repo.get(obj.__state__.id)
    assert stored is not None
    assert stored.__state__.version == 1
    stored.accept()
    assert stored.__state__.is_dirty()
    await repo.persist(stored)

    stored = await repo.get(obj.__state__.id)
    assert stored is not None
    assert stored.__state__.version == 2
    assert stored.is_accepted()


@pytest.mark.asyncio
async def test_repo_concurrent_write_is_rejected(
    factory: FulfillmentFactory,
    repo: FulfillmentRepository
) -> None:
    initial = factory.new(order_id=1)
    await repo.persist(initial)
    i1 = await repo.get(initial.__state__.id)
    i2 = await repo.get(initial.__state__.id)
    assert i1 is not None
    assert i2 is not None
    assert i1.__state__.id == i2.__state__.id

    i1.accept()
    await repo.persist(i1)

    i2.reject()
    with pytest.raises(StaleDomainObject):
        await repo.persist(i2)


@pytest.mark.asyncio
async def test_repo_get_with_no_id_returns_none(
    repo: FulfillmentRepository
) -> None:
    assert await repo.get(None) is None