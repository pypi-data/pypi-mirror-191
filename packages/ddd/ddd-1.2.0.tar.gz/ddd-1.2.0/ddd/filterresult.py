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
from typing import Generator
from typing import Awaitable
from typing import Generic
from typing import TypeVar

from .types import ICursor


T = TypeVar('T')


class FilterResult(Generic[T]):
    _cursor: ICursor[T] | Awaitable[ICursor[T]]
    token: str | None
    objects: list[T]
    limit: int

    def __init__(self, cursor: Awaitable[ICursor[T]]):
        self._cursor = cursor

    async def fetch(self) -> Any:
        if inspect.isawaitable(self._cursor):
            self._cursor = await self._cursor
            self.objects = self._cursor.all()
            self.token = self._cursor.get_pagination_token()
        return self

    def __aiter__(self) -> ICursor[T]:
        assert isinstance(self._cursor, ICursor)
        return self._cursor # type: ignore

    async def __anext__(self) -> T:
        raise NotImplementedError

    def __await__(self) -> Generator[None, None, Any]:
        return self.fetch().__await__()