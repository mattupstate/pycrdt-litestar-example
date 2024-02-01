import sys

import anyio
import dagger


async def test():
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        source_code = client.host().directory(
            ".", exclude=[".git", "node_modules", ".venv", "__ci__.py"]
        )

        javascript = (
            client.container()
            .from_("node:16.15.0-slim")
            .with_workdir("/src")
            .with_file("/src/package.json", client.host().file("package.json"))
            .with_file(
                "/src/package-lock.json", client.host().file("package-lock.json")
            )
            .with_exec(["npm", "install"])
            .with_directory("/src", source_code)
            .with_exec(["npx", "webpack", "--mode", "production"])
        )

        await javascript.sync()

        redis = client.container().from_("redis:7").with_exposed_port(6379).as_service()

        python = (
            client.container()
            .from_("python:3.12")
            .with_service_binding("redis", redis)
            .with_exec(["pip", "install", "poetry"])
            .with_workdir("/src")
            .with_file("/src/poetry.lock", client.host().file("poetry.lock"))
            .with_file("/src/pyproject.toml", client.host().file("pyproject.toml"))
            .with_exec(["poetry", "install", "--only", "playwright"])
            .with_exec(["poetry", "run", "playwright", "install-deps"])
            .with_exec(["poetry", "run", "playwright", "install", "chromium"])
            .with_directory("/src", source_code)
            .with_directory(
                "/src/example_app/static/bundles",
                javascript.directory("/src/example_app/static/bundles"),
            )
            .with_exec(["poetry", "install", "--without", "playwright"])
            .with_exec(["poetry", "run", "pytest"])
        )

        # execute
        await python.sync()

    print("Tests succeeded!")


anyio.run(test)
