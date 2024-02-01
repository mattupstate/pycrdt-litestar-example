import asyncio

import uvicorn

from example_app.factory import AppConfig, create_app


_default_app_config = AppConfig()


def run_server(
    host: str = "0.0.0.0",
    port: int = 8000,
    reload: bool = False,
    log_level: str = "info",
    app_config: AppConfig = _default_app_config,
):
    server = uvicorn.Server(
        uvicorn.Config(
            app=create_app(app_config),
            host=host,
            port=port,
            log_level=(log_level.lower()),
            reload=reload,
        )
    )
    asyncio.run(server.serve())
