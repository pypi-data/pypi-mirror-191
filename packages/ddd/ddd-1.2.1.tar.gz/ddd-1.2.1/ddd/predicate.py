# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import enum
from typing import Any

from .aggregatemeta import AggregateMeta
from .predicateoperator import PredicateOperator


class Predicate:
    __module__: str = 'ddd'
    name: str
    operator: PredicateOperator
    value: Any

    def __init__(self, name: str, operator: PredicateOperator, value: Any):
        self.name = name
        self.operator = operator
        self.value = value
        if isinstance(value, enum.Enum): # TODO
            self.value = value.value

    def can_apply(self, meta: AggregateMeta) -> bool:
        """Return a boolean indicating if the predicate can be applied
        to the given model.
        """
        return meta.has_field(self.name)

    def __repr__(self) -> str:
        return f'Predicate({self.name} {self.operator} {repr(self.value)})'

    def __and__(self, y: Any) -> 'And':
        if not isinstance(y, Predicate):
            raise TypeError(f"Unsupported operand & for '{type(y).__name__}'")
        return And([self, y])

    def __rand__(self, y: Any) -> 'And':
        return self.__and__(y)


class PaginationToken:

    def __init__(self, value: str):
        self.value = value


class And:
    __module__: str = 'ddd.predicate'
    predicates: list[Predicate]

    def __init__(self, predicates: list[Predicate]):
        self.predicates = predicates