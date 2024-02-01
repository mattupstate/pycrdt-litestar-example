import sys

import anyio
import dagger


async def test():
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        source = client.host().directory(
            ".", exclude=[".git", "node_modules", ".venv", "__ci__.py"]
        )
        redis = client.container().from_("redis:7").with_exposed_port(6379).as_service()

        python = (
            client.container()
            .from_("python:3.12-slim")
            .with_mounted_cache(
                "/root/.cache", client.cache_volume("pycrdt-example-app-cache")
            )
            .with_service_binding("redis", redis)
            .with_exec(
                [
                    "/bin/sh",
                    "-c",
                    "apt-get update && apt-get install --no-install-recommends -y build-essential",
                ]
            )
            .with_exec(["pip", "install", "poetry"])
            .with_workdir("/src")
            .with_file("/src/poetry.lock", client.host().file("poetry.lock"))
            .with_file("/src/pyproject.toml", client.host().file("pyproject.toml"))
            .with_exec(["poetry", "install", "--only", "playwright"])
            .with_exec(["poetry", "run", "playwright", "install-deps"])
            .with_exec(["poetry", "run", "playwright", "install", "chromium"])
            .with_directory("/src", source)
            .with_exec(["poetry", "install", "--without", "playwright"])
            .with_exec(["poetry", "run", "pytest"])
        )

        # execute
        await python.sync()

    print("Tests succeeded!")


anyio.run(test)
