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
from email.utils import format_datetime
from http import HTTPStatus as HTTP

from no_comment.application.use_cases import view_comments
from no_comment.domain.commenting import entities
from no_comment.interfaces.to_http import HttpPresenter


class XmlPresenter(HttpPresenter):
    def __init__(self, content_type: str = "application/xml") -> None:
        self.__status_code: HTTP = HTTP.OK
        self.__headers: dict[str, str] = {"Content-Type": content_type}
        self.__data: str = ""

    def status_code(self) -> int:
        return int(self.__status_code)

    def headers(self) -> dict[str, str]:
        return self.__headers

    def data(self) -> str:
        return self.__data


class StreamAsAtom(view_comments.Presenter, XmlPresenter):
    def __init__(self, id: str, title: str, url: str, author: str) -> None:
        super().__init__("application/atom+xml;charset=utf-8")
        self.__id = id
        self.__title = title
        self.__url = url
        self.__author = author
        self.__entries: str = ""
        self.__updated_on: str = "1970-01-01T00:00:00+00:00"

    def data(self) -> str:
        return f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    <id>{self.__id}</id>
    <title>{self.__title}</title>
    <link rel="self" type="application/atom+xml" href="{self.__url}" />
    <link rel="alternate" type="text/html" href="{self.__id}" />
    <updated>{self.__updated_on}</updated>
    <author>
        <name>{self.__author}</name>
    </author>
    <link href="http://creativecommons.org/licenses/by-sa/1.0/legalcode" rel="license" />
    {self.__entries}
</feed>"""

    def comment(self, comment: entities.Comment) -> None:
        updated_on = comment.created.to_isoformat(with_microseconds=False)
        if updated_on > self.__updated_on:
            self.__updated_on = updated_on
        self.__entries += f"""
    <entry>
        <id>{comment.id}</id>
        <title>{comment_title(comment)}</title>
        <link rel="external" href="{comment.url}" />
        <updated>{updated_on}</updated>
        <summary>{comment.text}</summary>
    </entry>"""


class StreamAsRss(view_comments.Presenter, XmlPresenter):
    def __init__(self, title: str, description: str, url: str) -> None:
        super().__init__("application/rss+xml;charset=utf-8")
        self.__title = title
        self.__description = description
        self.__url = url
        self.__items: str = ""
        self.__updated_on = datetime(1970, 1, 1, 0, 0, 0).astimezone(timezone.utc)

    def data(self) -> str:
        return f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
    <channel>
        <title>{self.__title}</title>
        <description>{self.__description}</description>
        <lastBuildDate>{format_datetime(self.__updated_on)}</lastBuildDate>
        <link rel="alternate" type="text/html" href="{self.__url}" />
        {self.__items}
    </channel>
</rss>"""

    def comment(self, comment: entities.Comment) -> None:
        updated_on = comment.created.to_datetime()
        if updated_on > self.__updated_on:
            self.__updated_on = updated_on
        self.__items += f"""
        <item>
            <title>{comment_title(comment)}</title>
            <link rel="external">{comment.url}</link>
            <description>{comment.text}</description>
            <pubDate>{format_datetime(updated_on)}</pubDate>
            <guid>{comment.id}</guid>
        </item>"""


def comment_title(comment: entities.Comment) -> str:
    TITLE_MAX_LENGTH = 30

    title = str(comment.text).split("\n")[0]
    if len(title) > TITLE_MAX_LENGTH:
        return title[0 : TITLE_MAX_LENGTH - 1] + "…"
    return title
