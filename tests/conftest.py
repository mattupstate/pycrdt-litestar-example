import socket

from dataclasses import dataclass
from multiprocessing import Process

import pytest

from testcontainers.redis import RedisContainer

from example_app.server import run_server


@dataclass
class ServerInfo:
    uri: str
    port: int


def random_port():
    sock = socket.socket()
    sock.bind(("", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


@pytest.fixture(scope="session")
def redis_server() -> ServerInfo:
    port = random_port()
    container = RedisContainer().with_bind_ports(6379, port)
    container.start()
    yield ServerInfo(uri=f"redis://127.0.0.1:{port}/0", port=port)
    container.stop()


@pytest.fixture(scope="session")
def app_server(redis_server: ServerInfo) -> ServerInfo:
    port = random_port()
    proc = Process(
        target=run_server,
        kwargs={
            "host": "127.0.0.1",
            "port": port,
            "redis_uri": redis_server.uri,
            "debug": True,
            "reload": False,
            "log_level": "debug",
        },
        daemon=True,
    )
    proc.start()
    yield ServerInfo(uri=f"http://127.0.0.1:{port}", port=port)
    proc.kill()
