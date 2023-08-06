# Copyright (C) 2022-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
from typing import Any

import pydantic


class AggregateState(pydantic.BaseModel):
    __module__: str = 'ddd'
    id: int | str | None = None

    created: datetime.datetime = pydantic.Field(
        default_factory=datetime.datetime.utcnow
    )

    dirty: bool = False

    version: int = pydantic.Field(
        default=0
    )

    spec: Any = None

    def dict(self, **kwargs: Any) -> dict[str, Any]:
        exclude = kwargs.setdefault('exclude', set())
        exclude.add('dirty')
        return super().dict(**kwargs)

    def increment(self) -> None:
        """Increment the version number by one."""
        self.version = self.version + 1

    def init(self, **kwargs: Any) -> None:
        """Initialize the state with the given keyword parameters."""
        assert self.spec is None # nosec
        field = self.__fields__['spec']
        self.spec = field.type_.parse_obj(kwargs)

    def is_dirty(self) -> bool:
        """Return a boolean indicating if the state is dirty."""
        return self.dirty or not self.id

    def set(self, attname: str, value: Any) -> None:
        """Set a property in the state."""
        if getattr(self.spec, attname) != value:
            setattr(self.spec, attname, value)
            self.dirty = True