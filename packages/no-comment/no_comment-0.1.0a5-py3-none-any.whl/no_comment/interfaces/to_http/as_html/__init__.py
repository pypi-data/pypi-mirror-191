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

from http import HTTPStatus as HTTP
from pathlib import Path
from typing import Any, Callable

from jinja2 import Environment, FileSystemLoader, select_autoescape

from no_comment.application.use_cases import add_comment, view_comments
from no_comment.domain.commenting import entities
from no_comment.domain.commenting import entities as e
from no_comment.interfaces.to_http import HttpPresenter

ENVIRONMENT = Environment(
    loader=FileSystemLoader([Path(__file__).parent / "templates"]),
    autoescape=select_autoescape(),
    extensions=["pypugjs.ext.jinja.PyPugJSExtension"],
)


def register_jinja_global(key: str, value: Any) -> None:
    ENVIRONMENT.globals[key] = value


class JinjaPresenter(HttpPresenter):
    def __init__(self, template: str, **context: Any) -> None:
        self.__status_code = HTTP.OK
        self.__headers = {"Content-Type": "text/html; charset=UTF-8"}
        self.__template = template
        self.__context = context
        self.__error = ""

    def status_code(self) -> int:
        return int(self.__status_code)

    def headers(self) -> dict[str, str]:
        return self.__headers

    def data(self) -> str:
        return self.render()

    def set_status_code(self, status_code: HTTP) -> None:
        self.__status_code = status_code

    def error(self, message: str, status_code: HTTP) -> None:
        self.__error = message
        self.__status_code = status_code

    def access_not_allowed(self, login: str) -> None:
        if login:
            self.__status_code = HTTP.FORBIDDEN
            self.__error = "You cannot access this page!"
        else:
            self.__status_code = HTTP.UNAUTHORIZED
            self.__error = "You must be logged in to access this page!"

    def render(self, **context: Any) -> str:
        if self.__error:
            return ENVIRONMENT.get_template("error.pug").render(message=self.__error)
        return ENVIRONMENT.get_template(self.__template).render(
            **self.__context, **context
        )


class PugPresenter(JinjaPresenter):
    def __init__(self, template: str, **context: Any) -> None:
        super().__init__(template + ".pug", **context)


class UnknownFormat(view_comments.Presenter, PugPresenter):
    def __init__(self) -> None:
        super().__init__("unknown_format")
        self.set_status_code(HTTP.NOT_FOUND)

    def comment(self, comment: entities.Comment) -> None:
        pass


class Stream(view_comments.Presenter, PugPresenter):
    def __init__(self, stream_id: str) -> None:
        super().__init__("stream")
        self.__context: dict[str, Any] = {"stream_id": stream_id, "comments": []}

    def comment(self, comment: entities.Comment) -> None:
        self.__context["comments"].insert(
            0, {"url": str(comment.url), "text": str(comment.text)}
        )

    def render(self, **context: Any) -> str:
        return super().render(**self.__context, **context)


class Comment(PugPresenter):
    def __init__(self) -> None:
        super().__init__("comment")


class AddComment(add_comment.Presenter, HttpPresenter):
    def __init__(self, next_url: Callable[[], str]) -> None:
        self.__next_url = next_url
        self.__comment_id = ""

    def status_code(self) -> int:
        return HTTP.SEE_OTHER

    def headers(self) -> dict[str, str]:
        return {"Location": self.__next_url()}

    def data(self) -> str:
        return ""

    def bad_parameter(self, name: str, value: str) -> None:
        import logging

        logging.error("TODO: set flash message")

    def comment_added(self, comment: e.Comment) -> None:
        self.__comment_id = str(comment.id)
