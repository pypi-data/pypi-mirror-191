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

from flask import Flask, get_flashed_messages, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

import no_comment.interfaces.to_http.as_html as html_presenters
from no_comment import __version__

from .api_comments import blueprint as api_comments
from .comments import blueprint as comments


def build_app(config: dict[str, str]) -> Flask:
    app = Flask(
        __name__,
        static_url_path="/resources",
        static_folder="./static/",
    )

    configure(app, config)
    register_blueprints(app)
    register_globals()

    return app


def configure(app: Flask, config: dict[str, str]) -> None:
    if config.get("PROXIED", ""):
        app.wsgi_app = ProxyFix(  # type: ignore[assignment]
            app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
        )

    app.config.update(
        # SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )
    app.config.update(config)


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(api_comments, url_prefix="/api/")
    app.register_blueprint(comments, url_prefix="/")


def register_globals() -> None:
    html_presenters.register_jinja_global("version", __version__)
    html_presenters.register_jinja_global("url_for", url_for)
    html_presenters.register_jinja_global("get_flashed_messages", get_flashed_messages)
