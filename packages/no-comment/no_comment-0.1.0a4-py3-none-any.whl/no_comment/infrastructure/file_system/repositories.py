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

import json
from pathlib import Path

from no_comment.domain.commenting.entities import Comment
from no_comment.domain.commenting.repositories import Comments as InterfaceComments
from no_comment.domain.commenting.value_objects import (
    CommentId,
    DateAndTime,
    StreamId,
    Text,
    Url,
)


class Comments(InterfaceComments):
    def __init__(self, data_dir: Path) -> None:
        self.__data_dir = data_dir

    def on_stream(self, stream_id: StreamId) -> list[Comment]:
        path = self.__path_for(stream_id)
        if not path.exists():
            return []
        return [
            # TODO: decide what to do with bad data.
            Comment(
                CommentId(data.get("id", "")),
                Url(data.get("url", "")),
                Text(data.get("text", "")),
                DateAndTime.from_isoformat(
                    data.get("created", "1971-01-01T00:00:00+00:00")
                ),
            )
            for data in [json.loads(line) for line in path.read_text().splitlines()]
        ]

    def __path_for(self, stream_id: StreamId) -> Path:
        return self.__data_dir / f"{stream_id}.jsons"

    def add(self, stream_id: StreamId, comment: Comment) -> None:
        data = {
            "id": str(comment.id),
            "url": str(comment.url),
            "text": str(comment.text),
            "created": comment.created.to_isoformat(),
        }
        path = self.__path_for(stream_id)
        with path.open("a") as fh:
            fh.write(json.dumps(data))
            fh.write("\n")
