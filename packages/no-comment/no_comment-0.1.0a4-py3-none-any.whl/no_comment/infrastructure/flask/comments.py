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

from flask import Blueprint, Response, request, url_for

from no_comment.application.use_cases import add_comment, view_comments
from no_comment.infrastructure.flask.utils import presenter_to_response
from no_comment.interfaces.to_http import as_html as html_presenters
from no_comment.interfaces.to_http import as_json as json_presenters
from no_comment.interfaces.to_http import as_xml as xml_presenters

from . import services

blueprint = Blueprint("comments", __name__)


@blueprint.get("/<string:stream_id>")
@blueprint.get("/<string:stream_id>.<string:format>")
@presenter_to_response
def index(stream_id: str, format: str = "html") -> Response:
    presenter = select_presenter_for_view_comments(stream_id, format)
    interactor = view_comments.Interactor(presenter, services.comments())
    rq = view_comments.Request(stream_id, request.args.get("url", ""))
    interactor.execute(rq)
    return presenter


def select_presenter_for_view_comments(
    stream_id: str, format: str
) -> view_comments.Presenter:
    PRESENTERS = {
        "html": html_presenters.Stream(stream_id),
        "atom": xml_presenters.StreamAsAtom("ID", stream_id, "URL", "Author"),
        "rss": xml_presenters.StreamAsRss(stream_id, "Description", "URL"),
        "json": json_presenters.StreamAsJsonFeed(),
    }
    return PRESENTERS.get(format, html_presenters.UnknownFormat())


@blueprint.post("/<string:stream_id>")
@presenter_to_response
def index_POST(stream_id: str) -> Response:
    presenter = html_presenters.AddComment(
        lambda: url_for("comments.index", stream_id=stream_id),
    )
    interactor = add_comment.Interactor(
        presenter, services.comments(), services.calendar()
    )
    rq = add_comment.Request(
        stream_id, request.form.get("url", ""), request.form.get("text", "")
    )
    interactor.execute(rq)
    return presenter


@blueprint.get("/<string:stream_id>/<string:comment_id>")
@presenter_to_response
def comment(stream_id: str, comment_id: str) -> Response:
    return html_presenters.Comment()
