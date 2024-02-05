import dagger


class AppPipelineTasks:
    PYTHON_BASE_IMAGE = "python:3.12-slim@sha256:a64ac5be6928c6a94f00b16e09cdf3ba3edd44452d10ffa4516a58004873573e"
    NODE_BASE_IMAGE = "node:16.15.0-slim@sha256:989dc486196a861f0ccc6c72f2eb7a5d3edb3451f2325bb8e81702ae42ed40e1"

    def __init__(self, client: dagger.Client):
        self._client = client

    def _source(self) -> dagger.Directory:
        return self._client.host().directory(
            ".",
            exclude=[
                ".cache",
                ".git",
                ".github",
                ".task",
                ".venv",
                ".vscode",
                "dist",
                "etc",
                "node_modules",
                "test-results",
                ".dockerignore",
                ".gitignore",
                ".python-version",
                "Dockerfile",
                "Taskfile.yaml",
                "docker-compose.yaml",
                "webpack-stats.json",
                "*.tar",
            ],
        )

    async def webpack(self) -> dagger.Directory:
        webpack = await (
            self._client.container()
            .from_(self.NODE_BASE_IMAGE)
            .with_workdir("/src")
            .with_file("/src/package.json", self._client.host().file("package.json"))
            .with_file(
                "/src/package-lock.json", self._client.host().file("package-lock.json")
            )
            .with_exec(["npm", "install"])
            .with_directory("/src", self._source())
            .with_exec(["npx", "webpack", "--mode", "production"])
        ).sync()
        return webpack.directory("/src/dist/js")

    def _redis_service(self) -> dagger.Service:
        return (
            self._client.container()
            .from_("redis:7")
            .with_exposed_port(6379)
            .as_service()
        )

    def _python_builder(self) -> dagger.Container:
        """Returns a base image for building and testing needs."""

        apt_cache = self._client.cache_volume("apt")
        user_cache = self._client.cache_volume("user")
        project_cache = self._client.cache_volume("project")

        return (
            self._client.container()
            .from_(self.PYTHON_BASE_IMAGE)
            # Install system packages required for compiling dependencies
            .with_exec(["apt-get", "update"])
            .with_exec(
                [
                    "apt-get",
                    "install",
                    "-y",
                    "--no-install-recommends",
                    "build-essential",
                    "gcc",
                ]
            )
            # Install and configure dependency management tools
            .with_exec(["python", "-m", "pip", "install", "--upgrade", "pip"])
            .with_exec(["pip", "install", "poetry==1.7"])
            .with_exec(["poetry", "config", "virtualenvs.in-project", "true"])
            # Setup the workspace
            .with_workdir("/home/app")
            .with_file("poetry.lock", self._client.host().file("poetry.lock"))
            .with_file("pyproject.toml", self._client.host().file("pyproject.toml"))
            # Install the main dependency group
            .with_exec(["poetry", "install", "--only", "main"])
            # Update the PATH to include the virtualenv
            .with_env_variable("PATH", "/home/app/.venv/bin:$PATH", expand=True)
            # Mount the source into the work space
            .with_directory("/home/app", self._source())
            .with_mounted_cache("/root/.cache", user_cache)
            .with_mounted_cache("/home/app/.cache", project_cache)
            .with_mounted_cache("/var/cache/apt", apt_cache)
        )

    async def test(self, webpack_build_output: dagger.Directory) -> dagger.Container:
        return await (
            self._python_builder()
            .with_service_binding("redis", self._redis_service())
            .with_exec(["poetry", "install", "--only", "playwright"])
            .with_exec(["poetry", "run", "playwright", "install-deps"])
            .with_exec(["poetry", "run", "playwright", "install", "chromium"])
            .with_directory("/opt/app/static/js", webpack_build_output)
            .with_exec(["poetry", "install", "--without", "playwright"])
            .with_exec(["pytest"])
        ).sync()
