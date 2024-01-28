from dataclasses import dataclass
from multiprocessing import Process

import pytest
import uvicorn

from testcontainers.redis import RedisContainer

from example_app.asgi import app


@dataclass
class ServerInfo:
    uri: str
    port: int


@pytest.fixture(scope="session")
def redis_server() -> ServerInfo:
    container = RedisContainer()
    container.start()
    port = 6379
    yield ServerInfo(uri=f"redis://127.0.0.1:{port}", port=port)
    container.stop()


@pytest.fixture(scope="session")
def app_server(redis_server: ServerInfo) -> ServerInfo:
    port = 8000
    proc = Process(
        target=uvicorn.run,
        args=(app,),
        kwargs={"host": "127.0.0.1", "port": port, "log_level": "debug"},
        daemon=True,
    )
    proc.start()
    yield ServerInfo(uri=f"http://127.0.0.1:{port}", port=port)
    proc.kill()
