import asyncio

import uvicorn

from example_app.factory import AppOptions, create_app


def run_server(
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
