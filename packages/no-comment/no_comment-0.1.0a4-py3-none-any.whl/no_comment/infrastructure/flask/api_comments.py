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

from flask import Blueprint, Response, request

from no_comment.application.use_cases import add_comment, view_comments
from no_comment.infrastructure.flask.utils import presenter_to_response
from no_comment.interfaces.to_http import as_json as json_presenters

from . import services

blueprint = Blueprint("api_comments", __name__)


@blueprint.get("/<string:stream_id>")
@presenter_to_response
def index(stream_id: str) -> Response:
    presenter = json_presenters.ViewComments()
    interactor = view_comments.Interactor(presenter, services.comments())
    rq = view_comments.Request(stream_id, request.args.get("url", ""))
    interactor.execute(rq)
    return presenter


@blueprint.post("/<string:stream_id>")
@presenter_to_response
def index_POST(stream_id: str) -> Response:
    presenter = json_presenters.AddComment()
    interactor = add_comment.Interactor(
        presenter, services.comments(), services.calendar()
    )
    rq = add_comment.Request(
        stream_id,
        (request.get_json(silent=True) or {}).get("url", ""),
        (request.get_json(silent=True) or {}).get("text", ""),
    )
    interactor.execute(rq)
    return presenter
