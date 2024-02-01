from dataclasses import dataclass

from litestar import Litestar
from litestar.channels import ChannelsPlugin
from litestar.channels.backends.redis import RedisChannelsPubSubBackend
from litestar.static_files import StaticFilesConfig
from redis.asyncio import Redis
from example_app.etc import app_resource

from example_app.routes import index, ws
from example_app.templates import create_template_config


def create_redis_client(uri: str):
    return Redis.from_url(uri)


@dataclass
class AppConfig:
    debug: bool = False
    redis_uri: str = "redis://redis:6379/0"
    static_dir: str = "/opt/app/static"


def create_app(config: AppConfig):
    redis = create_redis_client(config.redis_uri)

    channels_plugin = ChannelsPlugin(
        backend=RedisChannelsPubSubBackend(redis=redis),
        arbitrary_channels_allowed=True,
        create_ws_route_handlers=False,
    )

    template_config = create_template_config(
        app_resource("templates"), config.static_dir
    )

    static_files_config = StaticFilesConfig(
        directories=[config.static_dir], path="/static"
    )

    return Litestar(
        [index, ws],
        debug=config.debug,
        template_config=template_config,
        static_files_config=[static_files_config],
        plugins=[channels_plugin],
    )
