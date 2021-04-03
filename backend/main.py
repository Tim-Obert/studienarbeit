import argparse
import asyncio
from datetime import datetime

import cv2

from motiondetection.motiondetector import MotionDetector
from tinydbconnector import TinyDBConnector
from models.camera import Camera
from frameserver import FrameServer
from websocketserver import WebsocketServer
from motiondetection.bsmotiondetector import BSMotionDetector, MotionDetectionResult
from motiondetection.persondetector import PersonDetector
from recorder import Recorder, RecordingTrigger
import api
import imutils

db = TinyDBConnector('data/db.json')
frameserver = FrameServer()
websocketserver = WebsocketServer(frameserver)
recorder = Recorder(frameserver)


async def run():
    db = TinyDBConnector('data/db.json')
    frameserver = FrameServer()
    websocketserver = WebsocketServer(frameserver)
    cameras = db.get_cameras()
    if cameras is not None:
        for cam in cameras:
            asyncio.create_task(frameserver.capture(cam))
        motiondetector = BSMotionDetector(db, frameserver)
        motiondetector.run().subscribe(on_next=lambda res: asyncio.create_task(motion_result_handler(res)))
    asyncio.create_task(websocketserver.run())
    asyncio.create_task(api.run(frameserver, db))


async def motion_result_handler(result: MotionDetectionResult):
    msg = "result from " + result.camera.name + ": " + str(result.motion) + " (Magnitude: " + str(
        result.intensity) + ")"
    print(msg)
    await websocketserver.broadcast_event("MotionResult", result)
    if result.motion:
        await recorder.capture_while_motion(result.camera, RecordingTrigger.MOTION, 10)
        pass


if (__name__ == "__main__"):
    asyncio.get_event_loop().create_task(run())
    asyncio.get_event_loop().run_forever()
