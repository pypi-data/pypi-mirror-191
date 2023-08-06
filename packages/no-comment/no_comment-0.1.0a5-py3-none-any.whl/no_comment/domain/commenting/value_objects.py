# No Comment --- Comment any resource on the web!
# Copyright © 2023 Bioneland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime, timezone
from typing import Type, TypeVar
from urllib.parse import urlparse

from bl3d import DateAndTime as DT
from bl3d import InvalidValue as BaseInvalidValue
from bl3d import String

TypeText = TypeVar("TypeText", bound="Text")
TypeUrl = TypeVar("TypeUrl", bound="Url")


class InvalidValue(BaseInvalidValue):
    pass


class DateAndTime(DT):
    # TODO: use the one available in bl3d > 0.3.0
    @classmethod
    def from_isoformat(cls, isoformat: str) -> "DateAndTime":
        dt = datetime.fromisoformat(isoformat)
        if not dt.tzinfo:
            raise InvalidValue(cls.__name__, "Must define a timezone.")
        return cls.instanciate(dt.astimezone(timezone.utc))

    # TODO: use the one available in bl3d > 0.3.0
    def to_isoformat(self, /, *, with_microseconds: bool = True) -> str:
        dt = self.to_datetime()
        if not with_microseconds:
            dt = dt.replace(microsecond=0)
        return dt.isoformat()


class UniversalUniqueIdentifier(String):
    MIN: int = 36
    MAX: int = 36


class StreamId(String):
    pass


class CommentId(UniversalUniqueIdentifier):
    pass


class Text(String):
    @classmethod
    def instanciate(cls: Type[TypeText], value: str) -> TypeText:
        _ = String.instanciate(value)

        if not value.strip():
            raise InvalidValue(cls.__name__, "Text cannot be empty!")

        return cls(value)

    def __repr__(self) -> str:
        text = str(self).replace("'", "\\'")
        if len(text) > 11:
            text = text[:5] + "…" + text[-5:]
        return f"Text('{text}')"


class Url(String):
    @classmethod
    def instanciate(cls: Type[TypeUrl], value: str) -> TypeUrl:
        _ = String.instanciate(value)

        url = urlparse(value)
        if not url.scheme or not url.netloc:
            raise InvalidValue(cls.__name__, f"Invalid URL! [{value}]")

        return cls(value)

    def __repr__(self) -> str:
        return f"Url('{str(self)}')"
