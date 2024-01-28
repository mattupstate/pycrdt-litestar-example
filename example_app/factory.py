from dataclasses import dataclass

from litestar import Litestar
from litestar.channels import ChannelsPlugin
from litestar.channels.backends.redis import RedisChannelsPubSubBackend
from litestar.static_files import StaticFilesConfig
from redis.asyncio import Redis

from example_app.etc import app_resource
from example_app.routes import index, ws
from example_app.templates import template_config


def create_redis_client(uri: str):
    return Redis.from_url(uri)


@dataclass
class AppOptions:
    redis_uri: str = "redis://redis:6379/0"


def create_app(options: AppOptions):
    redis = create_redis_client(options.redis_uri)

    channels_plugin = ChannelsPlugin(
        backend=RedisChannelsPubSubBackend(redis=redis),
        arbitrary_channels_allowed=True,
        create_ws_route_handlers=False,
    )

    return Litestar(
        [index, ws],
        template_config=template_config,
        static_files_config=[
            StaticFilesConfig(directories=[app_resource("static")], path="/static"),
        ],
        plugins=[channels_plugin],
    )
