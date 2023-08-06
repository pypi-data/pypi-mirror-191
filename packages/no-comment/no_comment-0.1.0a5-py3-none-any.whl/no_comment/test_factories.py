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

from no_comment.domain.commenting.entities import Comment
from no_comment.domain.commenting.value_objects import CommentId, DateAndTime, Text, Url


# FIXME `comment` is also defined as a fixture in `conftest.py`.
def comment() -> Comment:
    return Comment(
        CommentId.instanciate("00000000-0000-0000-0000-000000000000"),
        Url.instanciate("https://s.d.t/p"),
        Text.instanciate("The text of the comment."),
        DateAndTime.instanciate(datetime.now(timezone.utc)),
    )
