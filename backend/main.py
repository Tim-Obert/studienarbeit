import asyncio
from motiondetection.motiondetector import MotionDetector
from tinydbconnector import TinyDBConnector
from camera import Camera
from frameserver import FrameServer
from websocketserver import WebsocketServer
from motiondetection.bsmotiondetector import BSMotionDetector, MotionDetectionResult
from recorder import Recorder, RecordingTrigger
import api
import threading

db = TinyDBConnector('data/db.json')
frameserver = FrameServer()
websocketserver = WebsocketServer(frameserver)
recorder = Recorder(frameserver)

async def run():
    for cam in db.get_cameras():
        asyncio.create_task(frameserver.capture(cam))

    motiondetector = BSMotionDetector(db, frameserver)
    motiondetector.run().subscribe(on_next=lambda res: asyncio.create_task(motion_result_handler(res)))

    asyncio.create_task(websocketserver.run())
    asyncio.create_task(api.run(frameserver, db))
    #apithread = threading.Thread(target = lambda x: api.start(x), args=(frameserver,))
    #apithread.start()

async def motion_result_handler(result: MotionDetectionResult):
    msg = "result from " + result.camera.name + ": " + str(result.motion) + " (Magnitude: " + str(result.intensity) + ")"
    print(msg)
    await websocketserver.broadcast(msg)
    if result.motion:
        await recorder.start_capture(db.get_cameras()[0], RecordingTrigger.MOTION)

if (__name__ == "__main__"):
    asyncio.get_event_loop().create_task(run())
    asyncio.get_event_loop().run_forever()
