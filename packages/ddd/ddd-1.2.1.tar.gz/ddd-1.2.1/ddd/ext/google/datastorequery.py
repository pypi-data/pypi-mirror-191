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

from google.cloud.datastore import Query

from ddd import PaginationToken
from ddd import Predicate
from ddd import PredicateOperator


class DatastoreQuery:
    limit: int
    supports: set[PredicateOperator] = {
        PredicateOperator.eq
    }
    token: str | None

    def __init__(self, query: Query, limit: int = 100, token: str | None = None):
        self.limit = limit
        self.query = query
        self.token = token

    def add_filter(self, property_name: str, operator: str, value: Any) -> None:
        self.query.add_filter(property_name, operator, value) # type: ignore

    @functools.singledispatchmethod
    def add_predicate(self, p: Predicate) -> None:
        if p.operator not in self.supports:
            raise NotImplementedError
        if p.operator == PredicateOperator.eq:
            self.query.add_filter(f'spec.{p.name}', p.operator.value, p.value) # type: ignore

    @add_predicate.register
    def add_pagination_token(self, p: PaginationToken) -> None:
        self.token = p.value

    @add_predicate.register
    def add_pagination_token_from_string(self, p: str) -> None:
        self.token = p

    def fetch(self, *args: Any, **kwargs: Any):
        kwargs.setdefault('limit', self.limit)
        if self.token:
            kwargs.setdefault('start_cursor', bytes.fromhex(self.token))
        return self.query.fetch(*args, **kwargs) # type: ignore