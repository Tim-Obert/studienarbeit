import asyncio
from camera import Camera
from frameserver import FrameServer
from cameraregistry import CameraRegistry
from websocketserver import WebsocketServer
from motiondetection.bsmotiondetector import BSMotionDetector
import api
import threading


async def run():
    frameserver = FrameServer()
    cameraregistry = CameraRegistry()
    websocketserver = WebsocketServer(frameserver)

    # later: add via api and load from storage on startup

    for cam in cameraregistry.get_cameras():
        asyncio.create_task(frameserver.capture(cam))
    
    motiondetector = BSMotionDetector(cameraregistry, frameserver)
    motiondetector.on_result_handler = lambda result: print("result from " + result.camera['name'] + ": " + str(result.motion)) 
    asyncio.create_task(motiondetector.run())

    asyncio.create_task(websocketserver.run())
    asyncio.create_task(api.run(frameserver, cameraregistry))
    #apithread = threading.Thread(target = lambda x: api.start(x), args=(frameserver,))
    #apithread.start()
    
if (__name__ == "__main__"):
    asyncio.get_event_loop().create_task(run())
    asyncio.get_event_loop().run_forever()
