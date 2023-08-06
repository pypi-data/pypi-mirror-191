# Copyright (C) 2022-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Declares :class:`Factory`."""
from typing import Any
from typing import Generic
from typing import TypeVar

from .aggregatemeta import AggregateMeta
from .factorymetaclass import FactoryMetaclass


T = TypeVar('T')


class Factory(Generic[T], metaclass=FactoryMetaclass):
    """Provides an interface to (re)build domain objects."""
    __module__: str = 'ddd'
    __abstract__: bool = True
    meta: AggregateMeta
    model: type[T]

    def new(self, **kwargs: Any) -> T:
        return self.model(None, **kwargs)