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

from abc import ABC, abstractmethod
from dataclasses import dataclass

from no_comment.domain.commenting.entities import Comment
from no_comment.domain.commenting.repositories import Comments
from no_comment.domain.commenting.value_objects import StreamId, Url


@dataclass
class Request:
    stream_id: str
    url: str


class Presenter(ABC):
    @abstractmethod
    def comment(self, comment: Comment) -> None:
        ...


@dataclass
class Interactor:
    presenter: Presenter
    comments: Comments

    def execute(self, request: Request) -> None:
        url = Url(request.url)
        for comment in self.comments.on_stream(StreamId(request.stream_id)):
            if not request.url:
                self.presenter.comment(comment)
            elif comment.url == url:
                self.presenter.comment(comment)
