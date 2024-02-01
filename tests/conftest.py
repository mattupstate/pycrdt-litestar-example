from dataclasses import dataclass
from multiprocessing import Process

import pytest

from example_app.server import run_server


@dataclass
class ServerInfo:
    uri: str
    port: int


@pytest.fixture(scope="session")
def app_server() -> ServerInfo:
    proc = Process(
        target=run_server,
        daemon=True,
    )
    proc.start()
    yield ServerInfo(uri="http://127.0.0.1:8000", port=8000)
    proc.kill()
