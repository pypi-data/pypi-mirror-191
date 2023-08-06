# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import TypeVar

from .exc import StaleDomainObject


R = TypeVar('R')


def concurrent(retries: int) -> Callable[..., Any]:
    """Decorator that retries a function call in which a domain object
    is persisted and raises a stale error.
    """
    def decorator_factory(
        func: Callable[..., Awaitable[R]]
    ) -> Callable[..., Awaitable[R]]:
        @functools.wraps(func)
        async def f(*args: Any, **kwargs: Any) -> R:
            n = 0
            while True:
                try:
                    result = await func(*args, **kwargs)
                    break
                except StaleDomainObject:
                    n += 1
                    if n >= retries:
                        raise
                    continue
            return result
        return f
    return decorator_factory