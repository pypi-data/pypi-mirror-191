# Copyright (C) 2022-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
import hashlib
from typing import cast
from typing import Any

import pydantic


class Event(pydantic.BaseModel):
    aggregate_id: int | str | None = None
    checksum: str | None = None
    data: dict[str, Any]
    id: int | str | None = None
    version: int

    def calculate_checksum(self, event: Any) -> None:
        """Calculcates the checksum for this event. The `event` parameter
        is the event previous to this event.
        """
        assert self.aggregate_id is not None
        data = self.dict(exclude={'id', 'checksum'})
        event = cast(Event, event)
        if not event:
            self.checksum = bytes.hex(self._hash(data))
            return
        assert isinstance(event, Event)
        assert event.checksum is not None
        assert len(event.checksum) == 64
        assert event.version == (self.version - 1)
        h = hashlib.sha3_256()
        h.update(bytes.fromhex(event.checksum))
        h.update(self._hash(data))
        self.checksum = bytes.hex(h.digest())

    @staticmethod
    def _hash(obj: Any) -> bytes:
        h = hashlib.sha3_256()
        if isinstance(obj, pydantic.BaseModel):
            for field in obj.__fields__.keys():
                v = getattr(obj, field)
                h.update(Event._hash(v))
        elif isinstance(obj, str):
            h.update(str.encode(obj, encoding='utf-8'))
        elif isinstance(obj, int):
            h.update(
                int.to_bytes(obj, (obj.bit_length() + 7) // 8, 'big')
            )
        elif isinstance(obj, dict):
            for key in sorted(obj.keys()): # type: ignore
                assert isinstance(key, str)
                h.update(Event._hash(key))
                h.update(Event._hash(obj[key]))
        elif isinstance(obj, list):
            for item in obj: # type: ignore
                h.update(Event._hash(item))
        elif isinstance(obj, datetime.datetime):
            h.update(Event._hash(obj.isoformat()))
        elif obj is None:
            pass
        else:
            raise TypeError(f'Unhashable type: {repr(obj)}')
        return h.digest()