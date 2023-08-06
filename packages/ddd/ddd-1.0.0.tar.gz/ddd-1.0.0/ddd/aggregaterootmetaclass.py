# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import TypeVar

import pydantic

from .aggregatemeta import AggregateMeta
from .aggregatestate import AggregateState
from .aggregatestatedescriptor import AggregateStateDescriptor


M = TypeVar('M', bound='AggregateRootMetaclass')


class AggregateRootMetaclass(type):
    state: type[AggregateState] = AggregateState

    def __new__(
        cls: type[M],
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **params: dict[str, Any]
    ) -> M:
        if not namespace.pop('__abstract__', False):
            # Find all annotated attributes. These are considered attributes
            # of the models' state. Construct a pydantic model to hold the
            # state.
            annotations = namespace.get('__annotations__') or {}
            fields = {
                k: namespace[k]
                for k in annotations.keys()
                if k in namespace and not str.startswith(k, '_')
            }
            StateModel = type(f'{name}State', (pydantic.BaseModel,), {
                '__annotations__': annotations,
                **fields
            })

            # Initialize the meta class for the aggregate.
            namespace['__meta__'] = AggregateMeta(
                name=name,
                model=type(cls.state.__name__, (cls.state,), {
                    '__annotations__': {'spec': None | StateModel},
                    'spec': pydantic.Field(None)
                })
            )

            # Create a descriptor for each property. These control
            # access to the state. Normally these arent accessed
            # directly, unless by components that have internal access
            # to the domain object, such as factories or repositories.
            for k in annotations.keys():
                namespace[k] = AggregateStateDescriptor(k)

        return super().__new__(cls, name, bases, namespace, **params)