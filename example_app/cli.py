import click

from example_app.factory import AppConfig
from example_app.logging import configure_logging
from example_app.server import run_server


@click.group()
def cli():
    pass


@cli.command(help="Run the web server")
@click.option("--host", default="0.0.0.0", help="Host to bind to")
@click.option("--port", default=8000, help="Port to bind to")
@click.option("--debug", is_flag=True, default=False, help="Enable debug mode")
@click.option("--reload", is_flag=True, default=False, help="Reload code on changes")
@click.option("--log-level", default="info", help="Log level")
@click.option(
    "--static-dir",
    default="/opt/app/static",
    help="Filesystem path to static files directory",
)
def run(
    host: str, port: int, debug: bool, reload: bool, log_level: str, static_dir: str
):
    configure_logging(log_level)
    run_server(
        host, port, reload, log_level, AppConfig(debug=debug, static_dir=static_dir)
    )
