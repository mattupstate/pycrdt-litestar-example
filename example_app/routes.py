import structlog

from litestar import WebSocket, websocket, get
from litestar.channels import ChannelsPlugin
from litestar.response import Template
from pycrdt import Doc
from pycrdt_websocket.websocket import Websocket as PyCRDTWebSocket
from pycrdt_websocket.yutils import YMessageType, sync, process_sync_message

log: structlog.BoundLogger = structlog.get_logger()

documents = {}


@get("/")
async def index() -> Template:
    return Template(template_name="index.html", context={})


@websocket("/ws/{channel:str}")
async def ws(channel: str, socket: WebSocket, channels: ChannelsPlugin) -> None:
    await socket.accept()

    async def _publish(data: bytes):
        channels.publish(data, channel)

    socket_adapter = _WebSocketAdapter(f"/ws/{channel}", _publish)

    if channel not in documents:
        documents[channel] = Doc()
    doc = documents[channel]
    await sync(doc, socket_adapter, log)

    async def on_channel_message(data: bytes):
        await socket.send_bytes(data)

    async def on_websocket_message(data: bytes):
        channels.publish(data, channel)
        if data[0] == YMessageType.SYNC:
            await process_sync_message(data[1:], doc, socket_adapter, log)

    async with channels.start_subscription([channel]) as subscriber:
        async with subscriber.run_in_background(on_channel_message):
            async for data in socket.iter_data(mode="bytes"):
                await on_websocket_message(data)


class _WebSocketAdapter(PyCRDTWebSocket):
    def __init__(self, path, send_func) -> None:
        self._path = path
        self._send_func = send_func

    @property
    def path(self) -> str:
        return self._path

    def __aiter__(self):
        raise NotImplementedError()

    async def __anext__(self) -> bytes:
        raise NotImplementedError()

    async def send(self, message: bytes) -> None:
        await self._send_func(message)

    async def recv(self) -> bytes:
        raise NotImplementedError()
