import os
from frameserver import FrameServer
from cameraregistry import CameraRegistry
from flask import Flask, render_template, Response, request, jsonify
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer
import uuid
import json
import cv2 as cv
from PIL import Image
from base64 import b64encode
import io

app = Flask(__name__)

frameserver = None
cameraregistry = None
pcs = set()

def generate(name):
    while True:
        frame = frameserver.get_frame_jpeg(name)
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame) + b'\r\n')

def multi(request):
    return web.Response(content_type="application/json", text="{}")

def test(request):
    content = open(os.path.join(os.path.dirname(__file__), "templates/test.html"), "r").read()
    return web.Response(content_type="text/html", text=content)

async def test2(request):
    last = frameserver.get_buffer("Cam1").get_buffer()[0]
    if (last == None):
        return web.Response(content_type="text/html", text="No Frame")
    output = io.BytesIO()
    frame = last.to_image()
    frame.save(output, format='PNG')
    output.seek(0)
    output_s = output.read()
    b64 = b64encode(output_s)
    return web.Response(content_type="text/html", text="<img src='data:image/png;base64," + str(b64)[2:-1] + "'>")

@app.route("/streams/<name>")
def single(name):
    return Response(generate(name),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

async def buffer(request):
    return web.Response(content_type="text/plain", text=str(frameserver.get_buffer("Cam1").get_buffer()))

async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        print("ICE connection state is %s" % pc.iceConnectionState)
        if pc.iceConnectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    cam = cameraregistry.get_camera_by_name(params['name'])
    player = frameserver.get_player(cam.name)#MediaPlayer(cam.url, options={"rtsp_transport": "tcp"})
    print(player)

    await pc.setRemoteDescription(offer)
    for t in pc.getTransceivers():
        if t.kind == "audio" and player.audio:
            pc.addTrack(player.audio)
        elif t.kind == "video" and player.video:
            pc.addTrack(player.video)

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        text=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
    )

async def run(fs: FrameServer, cr: CameraRegistry):
    global frameserver, cameraregistry
    frameserver = fs
    cameraregistry = cr

    app = web.Application()
    app.router.add_get("/", multi)
    app.router.add_get("/test", test)
    app.router.add_get("/test2", test2)
    app.router.add_get("/buffer", buffer)
    app.router.add_post("/webrtc/offer", offer)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 5000)    
    await site.start()