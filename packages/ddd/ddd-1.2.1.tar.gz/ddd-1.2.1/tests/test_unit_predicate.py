# Copyright (C) 2022-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import cast

from ddd import Predicate
from ddd import PredicateOperator
from ddd.predicate import And
from ddd.test import Fulfillment


def test_eq():
    p = cast(Predicate, Fulfillment.order_id == 1)
    assert isinstance(p, Predicate)
    assert p.name == 'order_id'
    assert p.operator == PredicateOperator.eq
    assert p.value == 1


def test_and():
    p = cast(And, (Fulfillment.order_id == 1) & (Fulfillment.order_id == 2))
    assert isinstance(p, And)
    assert p.predicates[0].value == 1
    assert p.predicates[1].value == 2