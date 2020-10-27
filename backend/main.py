import asyncio
from camera import Camera
from frameserver import FrameServer
from cameraregistry import CameraRegistry
from websocketserver import WebsocketServer
import api
import threading   

async def run():

    frameserver = FrameServer()
    cameraregistry = CameraRegistry()
    websocketserver = WebsocketServer(frameserver)

    cameraregistry.add_camera(Camera("Cam1", "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"))

    asyncio.create_task(frameserver.capture(cameraregistry.get_camera_by_name("Cam2")))

    asyncio.create_task(websocketserver.run())
    asyncio.create_task(api.run(frameserver, cameraregistry))
    #apithread = threading.Thread(target = lambda x: api.start(x), args=(frameserver,))
    #apithread.start()

if (__name__ == "__main__"):
    asyncio.get_event_loop().create_task(run())
    asyncio.get_event_loop().run_forever()