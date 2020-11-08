from frameserver import FrameServer
import websockets
import json

class WebsocketServer:
    frameserver = None

    def __init__(self, fs: FrameServer):
        self.frameserver = fs

    async def __websocket_cb(self, websocket, path):
        while True:
            data = [self.frameserver.get_frame_jpeg(x) for x in self.frameserver.buff.keys()]
            await websocket.send(json.dumps(data))

    async def run(self):
        ws_server = await websockets.serve(self.__websocket_cb, "127.0.0.1", 5678)
        await ws_server.wait_closed()