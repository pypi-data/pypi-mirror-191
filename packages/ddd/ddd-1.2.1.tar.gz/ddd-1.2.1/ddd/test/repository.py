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
from .fulfillment import Fulfillment
from .fulfillment import FulfillmentStatus
from .fulfillmentfactory import FulfillmentFactory
from .fulfillmentrepository import FulfillmentRepository


__all__: list[str] = [
    'test_repo_new_persist_get',
    'test_repo_persist_updates_version',
    'test_repo_concurrent_write_is_rejected',
    'test_repo_get_with_no_id_returns_none',
    'test_repo_persists_state',
    'test_repo_persists_state_on_existing_object',
    'test_repo_find_by_predicate',
    'test_repo_find_by_predicate_from_multiple',
    'test_repo_find_by_multiple_predicate',
    'test_repo_filter_eq',
    'test_repo_filter_limit',
    'test_repo_iterate_cursor',
    'test_repo_paginate_cursor',
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


@pytest.mark.asyncio
async def test_repo_find_by_predicate(
    repo: FulfillmentRepository,
    factory: FulfillmentFactory
) -> None:
    initial = factory.new(order_id=1)
    await repo.persist(initial)

    result = await repo.find(Fulfillment.order_id==1)
    assert result is not None
    assert result.__state__.id == initial.__state__.id


@pytest.mark.asyncio
async def test_repo_find_by_predicate_from_multiple(
    repo: FulfillmentRepository,
    factory: FulfillmentFactory
) -> None:
    initial = factory.new(order_id=1)
    await repo.persist(initial)
    await repo.persist(factory.new(order_id=2))
    await repo.persist(factory.new(order_id=3))

    result = await repo.find(Fulfillment.order_id==1)
    assert result is not None
    assert result.__state__.id == initial.__state__.id

    # Does not find object that doesnt match the predicate.
    result = await repo.find(Fulfillment.status==FulfillmentStatus.accepted)
    assert result is None


@pytest.mark.asyncio
async def test_repo_find_by_multiple_predicate(
    repo: FulfillmentRepository,
    factory: FulfillmentFactory
) -> None:
    initial = factory.new(order_id=1)
    await repo.persist(initial)

    result = await repo.find(
        Fulfillment.order_id==1,
        Fulfillment.status==FulfillmentStatus.detected
    )
    assert result is not None
    assert result.__state__.id == initial.__state__.id

    # Check if it does not return an object that does not
    # match the predicate.
    result = await repo.find(
        Fulfillment.order_id==1,
        Fulfillment.status==FulfillmentStatus.accepted
    )
    assert result is None


@pytest.mark.asyncio
async def test_repo_filter_eq(
    repo: FulfillmentRepository,
    factory: FulfillmentFactory
):
    if not repo.can_filter():
        pytest.skip()
    await repo.persist(factory.new(order_id=1))
    await repo.persist(factory.new(order_id=2))
    obj = await repo.persist(factory.new(order_id=3))
    obj.accept()
    await repo.persist(obj)

    result = await repo.filter(
        Fulfillment.status==FulfillmentStatus.detected
    )
    assert len(result.objects) == 2

    result = await repo.filter(
        Fulfillment.status==FulfillmentStatus.accepted
    )
    assert len(result.objects) == 1
    assert isinstance(result.objects[0], Fulfillment), result.objects[0]


@pytest.mark.asyncio
async def test_repo_filter_limit(
    repo: FulfillmentRepository,
    factory: FulfillmentFactory
):
    if not repo.can_filter():
        pytest.skip()

    n = 3
    l = 2
    for order_id in range(1, n):
        await repo.persist(factory.new(order_id=order_id))

    result = await repo.filter(
        Fulfillment.status==FulfillmentStatus.detected,
        limit=l
    )
    assert len(result.objects) == (l), len(result.objects)
    assert isinstance(result.objects[0], Fulfillment), result.objects[0]


@pytest.mark.asyncio
async def test_repo_iterate_cursor(
    repo: FulfillmentRepository,
    factory: FulfillmentFactory
):
    if not repo.can_filter():
        pytest.skip()
    n = 11
    for order_id in range(1, n + 1):
        await repo.persist(factory.new(order_id=order_id))

    result = await repo.filter(Fulfillment.status==FulfillmentStatus.detected)
    assert isinstance(result.objects[0], Fulfillment), result.objects[0]

    seen = 0
    async for _ in result:
        seen += 1
    assert seen == n


@pytest.mark.asyncio
async def test_repo_paginate_cursor(
    repo: FulfillmentRepository,
    factory: FulfillmentFactory
):
    if not repo.can_filter():
        pytest.skip()
    n = 11
    for order_id in range(1, n + 1):
        await repo.persist(factory.new(order_id=order_id))

    result = await repo.filter(
        Fulfillment.status==FulfillmentStatus.detected,
        limit=5
    )
    assert len(result.objects) == 5
    assert result.token is not None
    assert isinstance(result.objects[0], Fulfillment), result.objects[0]
    result = await repo.filter(result.token, limit=5)
    assert len(result.objects) == 5, result.objects
    assert result.token is not None
    result = await repo.filter(result.token, limit=5)
    assert len(result.objects) == 1, len(result.objects)
    assert result.token is None, result.token