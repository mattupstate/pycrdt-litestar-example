import asyncio

import click
import uvicorn

from example_app.logging import configure_logging
from example_app.server import run_server


@click.group()
def cli():
    pass


@cli.command(help="Run the web server")
@click.option("--host", default="0.0.0.0", help="Host to bind to")
@click.option("--port", default=8000, help="Port to bind to")
@click.option("--redis-uri", default="redis://redis:6379/0", help="Redis URI")
@click.option("--debug", is_flag=True, default=False, help="Enable debug mode")
@click.option("--reload", is_flag=True, default=False, help="Reload code on changes")
@click.option("--log-level", default="info", help="Log level")
def run(
    host: str, port: int, redis_uri: str, debug: bool, reload: bool, log_level: str
):
    configure_logging(log_level)
    run_server(host, port, redis_uri, debug, reload, log_level)
