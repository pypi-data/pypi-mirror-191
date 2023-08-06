# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import get_args
from typing import Any
from typing import TypeVar

from .aggregateroot import AggregateRoot


M = TypeVar('M', bound='RepositoryMetaclass')


class RepositoryMetaclass(type):
    model: AggregateRoot

    def __new__(
        cls: type[M],
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **params: dict[str, Any]
    ) -> M:
        if not namespace.pop('__abstract__', False):
            for parent in reversed(bases):
                # Find out if there is a Repository subclass in the parents,
                # and inherit the model from that. Assume that if a model
                # attribute is present, this is a base or interface class.
                if isinstance(parent, RepositoryMetaclass)\
                and hasattr(parent, 'model'):
                    model: type[AggregateRoot] = parent.model
                    break
            else:
                origins: tuple[type, ...] = namespace.get('__orig_bases__') or tuple()
                if not origins or len(origins) > 1: # pragma: no cover
                    raise TypeError(
                        f'Invalid bases for {name}: '
                        f'{repr(namespace.get("__orig__bases"))}'
                    )
                args: tuple[type, ...] = get_args(origins[0])
                if not args or len(args) > 1: # pragma: no cover
                    raise TypeError(f'Invalid type arguments for {name}')
                model: type[AggregateRoot] = args[0]

            annotations: dict[str, type] = namespace.get('__annotations__') or {}
            annotations['model'] = type[AggregateRoot]
            namespace['meta'] = model.__meta__
            namespace['model'] = model
        else:
            # Remove methods that need to be implemented by subclasses
            # to prevent complaints when using multiple bases.
            namespace.pop('flush', None)
            namespace.pop('restore', None)
        return super().__new__(cls, name, bases, namespace, **params)