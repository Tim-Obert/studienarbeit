import asyncio
from frameserver import FrameServer
import websockets
import json

class WebsocketServer:
    frameserver = None
    sockets = set()

    def __init__(self, fs: FrameServer):
        self.frameserver = fs

    async def __websocket_cb(self, websocket, path):
        self.sockets.add(websocket)
        while True:
            # keep connection alive
            await asyncio.sleep(10)

    async def broadcast(self, message: str):
        for socket in self.sockets:
            if socket.closed:
                self.sockets.remove(socket)
                break
            await socket.send(message)

    async def run(self):
        ws_server = await websockets.serve(self.__websocket_cb, "0.0.0.0", 5678)
        await ws_server.wait_closed()