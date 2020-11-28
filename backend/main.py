import asyncio
from tinydbconnector import TinyDBConnector
from models.camera import Camera
from frameserver import FrameServer
from websocketserver import WebsocketServer
from motiondetection.bsmotiondetector import BSMotionDetector
import api
import threading


async def run():
    db = TinyDBConnector('data/db.json')

    frameserver = FrameServer()
    websocketserver = WebsocketServer(frameserver)
    print(db.get_settings())

    for cam in db.get_cameras():
        asyncio.create_task(frameserver.capture(cam))

    motiondetector = BSMotionDetector(db, frameserver)
    #motiondetector.on_result_handler = lambda result: print("result from " + result.camera.name + ": " + str(result.motion)) 
    asyncio.create_task(motiondetector.run())

    asyncio.create_task(websocketserver.run())
    asyncio.create_task(api.run(frameserver, db))
    #apithread = threading.Thread(target = lambda x: api.start(x), args=(frameserver,))
    #apithread.start()
    
if (__name__ == "__main__"):
    asyncio.get_event_loop().create_task(run())
    asyncio.get_event_loop().run_forever()
