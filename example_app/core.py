import structlog

from litestar import WebSocket, websocket, get
from litestar.channels import ChannelsPlugin
from litestar.channels.backends.redis import RedisChannelsPubSubBackend
from litestar.response import Template
from pycrdt import Doc
from pycrdt_websocket.yutils import (
    YMessageType,
    YSyncMessageType,
    create_message,
    read_message,
)
from redis.asyncio import Redis

log: structlog.BoundLogger = structlog.get_logger()

redis: Redis = Redis.from_url("redis://localhost:6379/0")

channels_plugin = ChannelsPlugin(
    backend=RedisChannelsPubSubBackend(redis=redis),
    arbitrary_channels_allowed=True,
    create_ws_route_handlers=False,
)


async def sync(ydoc: Doc, socket: WebSocket):
    state = ydoc.get_state()
    msg = create_message(state, YSyncMessageType.SYNC_STEP1)
    await socket.send_bytes(msg)


async def process_sync_message(message: bytes, ydoc: Doc, websocket: WebSocket):
    message_type = message[0]
    msg = message[1:]
    if message_type == YSyncMessageType.SYNC_STEP1:
        state = read_message(msg)
        update = ydoc.get_update(state)
        reply = create_message(update, YSyncMessageType.SYNC_STEP2)
        await websocket.send_bytes(reply)
    else:
        update = read_message(msg)
        if update != b"\x00\x00":
            ydoc.apply_update(update)


@get("/")
async def index() -> Template:
    return Template(template_name="index.html", context={})


documents = {}


@websocket("/ws/{channel:str}")
async def ws(channel: str, socket: WebSocket, channels: ChannelsPlugin) -> None:
    await socket.accept()

    if channel not in documents:
        documents[channel] = Doc()
    doc = documents[channel]
    await sync(doc, socket)

    async def on_channel_message(message: bytes):
        try:
            await socket.send_bytes(message)
        except Exception:
            log.exception(
                "Unexpected error while handling message channel=%s message=%s",
                channel,
                message,
            )

    try:
        async with channels.start_subscription(
            [channel]
        ) as subscriber, subscriber.run_in_background(on_channel_message):
            log.debug("Subscribed to channel: %s", channel)
            async for data in socket.iter_data(mode="bytes"):
                channels.publish(data, channel)
                if data[0] == YMessageType.SYNC:
                    await process_sync_message(data[1:], documents[channel], socket)

    except Exception:
        log.exception("Unexpected error")
    finally:
        await channels.unsubscribe(subscriber)
        log.debug("Unsubscribed from channel: %s", channel)
