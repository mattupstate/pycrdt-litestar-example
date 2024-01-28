import asyncio

import click
import uvicorn

from example_app.factory import AppOptions, create_app
from example_app.logging import configure_logging


@click.group()
def cli():
    pass


@cli.command(help="Run the web server")
@click.option("--host", default="0.0.0.0", help="Host to bind to")
@click.option("--port", default=8000, help="Port to bind to")
@click.option("--redis-uri", default="redis://127.0.0.1:6379/0", help="Redis URI")
@click.option("--debug", is_flag=True, default=False, help="Enable debug mode")
@click.option("--reload", is_flag=True, default=False, help="Reload code on changes")
@click.option("--log-level", default="info", help="Log level")
def run(
    host: str, port: int, redis_uri: str, debug: bool, reload: bool, log_level: str
):
    configure_logging(log_level)
    _run(host, port, redis_uri, debug, reload, log_level)


def _run(
    host: str, port: int, redis_uri: str, debug: bool, reload: bool, log_level: str
):
    options = AppOptions(redis_uri=redis_uri)
    app = create_app(options)
    config = uvicorn.Config(
        app=app,
        host=host,
        port=port,
        log_level=(log_level.lower()),
        reload=reload,
    )
    server = uvicorn.Server(config)
    asyncio.run(server.serve())
