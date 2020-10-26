import asyncio
from camera import Camera
from frameserver import FrameServer
from cameraregistry import CameraRegistry
from websocketserver import WebsocketServer
import api
import threading   

async def run():

    frameserver = FrameServer()
    websocketserver = WebsocketServer(frameserver)

    asyncio.create_task(websocketserver.run())
    apithread = threading.Thread(target = lambda x: api.start(x), args=(frameserver,))
    apithread.start()

    cam1 = Camera("Cam1", "rtsp://127.0.0.1:8554/stream")
    cam2 = Camera("Cam2", "rtsp://127.0.0.1:8554/stream")

    asyncio.create_task(frameserver.capture(cam1))
    asyncio.create_task(frameserver.capture(cam2))

if (__name__ == "__main__"):
    asyncio.get_event_loop().create_task(run())
    asyncio.get_event_loop().run_forever()