from litestar import Litestar
from litestar.static_files import StaticFilesConfig

from example_app.etc import app_resource
from example_app.core import index, ws, channels_plugin
from example_app.logging import configure_logging
from example_app.templates import template_config

configure_logging()

app = Litestar(
    [index, ws],
    template_config=template_config,
    static_files_config=[
        StaticFilesConfig(directories=[app_resource("static")], path="/static"),
    ],
    plugins=[channels_plugin],
)
