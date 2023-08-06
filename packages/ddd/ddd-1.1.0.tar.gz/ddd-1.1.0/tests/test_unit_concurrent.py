# Copyright (C) 2022-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import collections

import pytest

import ddd


@pytest.mark.asyncio
async def test_concurrent_retries_until_success():
    counter = collections.Counter('n')
    result = "Success!"

    @ddd.utils.concurrent(2)
    async def f():
        if counter['n'] == 0:
            raise ddd.exc.StaleDomainObject
        counter.update('n')
        return result

    assert await f() == result


@pytest.mark.asyncio
async def test_concurrent_retries_until_maximum_retries():
    max_attempts = 5
    counter = collections.Counter('n')
    result = "Success!"

    @ddd.utils.concurrent(max_attempts)
    async def f():
        if counter['n'] < max_attempts:
            raise ddd.exc.StaleDomainObject
        counter.update('n')
        return result

    with pytest.raises(ddd.exc.StaleDomainObject):
        assert await f() == result