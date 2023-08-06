# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inspect
from typing import Any
from typing import AsyncGenerator
from typing import Awaitable
from typing import Callable
from typing import Generator
from typing import Generic
from typing import TypeVar

from .types import ICursor


M = TypeVar('M')
T = TypeVar('T')


class FilterResult(Generic[M, T]):
    _cursor: ICursor[T] | Awaitable[ICursor[T]]
    _reconstruct_model: Callable[[T], M]
    token: str | None
    objects: list[M]
    limit: int

    def __init__(self,
        reconstruct_model: Callable[[T], M],
        cursor: Awaitable[ICursor[T]]
    ):
        self._reconstruct_model = reconstruct_model
        self._cursor = cursor

    async def fetch(self) -> Any:
        if inspect.isawaitable(self._cursor):
            self._cursor = await self._cursor
            self.objects = [
                self._reconstruct_model(x) for x in self._cursor.all()
            ]
            self.token = self._cursor.get_pagination_token()
        return self

    async def iter(self) -> AsyncGenerator[M, None]:
        assert isinstance(self._cursor, ICursor)
        async for state in self._cursor: # type: ignore
            yield self._reconstruct_model(state) # type: ignore

    def __aiter__(self) -> ICursor[T]:
        assert isinstance(self._cursor, ICursor)
        return self.iter()

    async def __anext__(self) -> T:
        raise NotImplementedError

    def __await__(self) -> Generator[None, None, Any]:
        return self.fetch().__await__()