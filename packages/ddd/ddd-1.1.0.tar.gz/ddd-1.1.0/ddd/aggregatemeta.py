# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .aggregatestate import AggregateState


class AggregateMeta:
    """Describes the inner workings of a domain model."""
    __module__: str = 'ddd'
    model: type[AggregateState]
    name: str

    def __init__(
        self,
        name: str,
        model: type[AggregateState]
    ):
        self.name = name
        self.model = model