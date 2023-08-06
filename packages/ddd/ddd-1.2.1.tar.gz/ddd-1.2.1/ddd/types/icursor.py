# Copyright (C) 2022-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Generator
from typing import Generic
from typing import TypeVar


T = TypeVar('T')


class ICursor(Generic[T]):
    MultipleObjectsReturned: type[Exception] = type('MultipleObjectsReturned', (Exception,), {})

    def all(self) -> list[T]:
        """Return all objects matching the search criteria."""
        raise NotImplementedError

    async def fetch(self) -> 'ICursor[T]':
        raise NotImplementedError

    def get_pagination_token(self) -> str | None:
        raise NotImplementedError

    def one(self) -> None | T:
        raise NotImplementedError

    def __aiter__(self) -> 'ICursor[T]':
        return self

    async def __anext__(self) -> T:
        raise NotImplementedError

    def __await__(self) -> Generator[None, None, 'ICursor[T]']:
        return self.fetch().__await__()