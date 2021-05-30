import cv2

from dbconnector import DBConnector
import os
from videowriter import VideoWriter
from frameserver import FrameServer
from models.camera import Camera
from models.settings import Settings
from aiohttp import web, MultipartWriter
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer
import json
from base64 import b64encode
import io
import asyncio

frameserver = None
db = None
pcs = set()

async def multi(request):
    return web.Response(content_type="application/json", text="{}")

async def test(request):
    content = open(os.path.join(os.path.dirname(__file__), "templates/test.html"), "r").read()
    return web.Response(content_type="text/html", text=content)

async def save(request):
    buffer = frameserver.get_buffer("test")
    writer = VideoWriter("/home/hannes/Projekte/studienarbeit/test/out.mp4")
    writer.open()
    writer.write_packets(buffer.get_packets())
    subscription = buffer.get_observable().subscribe(on_next=lambda p: writer.write_packet(p))
    await asyncio.sleep(10)
    subscription.dispose()
    writer.close()

    last = buffer.get_packets()[-1]
    if (last == None):
        return web.Response(content_type="text/html", text="No Frame")
    output = io.BytesIO()
    frame = last.decode()[0].to_image()
    frame.save(output, format='PNG')
    output.seek(0)
    output_s = output.read()
    b64 = b64encode(output_s)
    return web.Response(content_type="text/html", text="<img src='data:image/png;base64," + str(b64)[2:-1] + "'>")

async def single_frame(request):
    name = request.match_info['name']
    response = web.StreamResponse(status=200, reason='OK', headers={
        'Content-Type': 'multipart/x-mixed-replace; '
                        'boundary=--frame',
    })
    await response.prepare(request)
    buffer = frameserver.get_buffer(name)
    last = 0
    while True:
        with MultipartWriter('image/jpeg', boundary="frame") as mpwriter:
            frame = buffer.get_latest_packet()
            if frame is not None:
                data = frame.to_image()

                img_byte_arr = io.BytesIO()
                data.save(img_byte_arr, format='JPEG')
                img_byte_arr = img_byte_arr.getvalue()

                mpwriter.append(img_byte_arr, {
                    'Content-Type': 'image/jpeg'
                })
                await mpwriter.write(response, False)
            await asyncio.sleep(1/15)
        await response.drain()
    return response

async def single(request):
    id = int(request.match_info['id'])
    response = web.StreamResponse(status=200, reason='OK', headers={
        'Content-Type': 'multipart/x-mixed-replace; '
                        'boundary=--frame',
    })
    await response.prepare(request)
    buffer = frameserver.get_buffer(id)
    last = 0
    while True:

        with MultipartWriter('image/jpeg', boundary="frame") as mpwriter:
            packet = buffer.get_latest_keyframe()
            if packet is not None and packet.pts > last:
                last = packet.pts
                frame = packet.decode()
                if len(frame) == 0:
                    continue
                data = frame[0].to_image()
                img_byte_arr = io.BytesIO()
                data.save(img_byte_arr, format='JPEG')
                img_byte_arr = img_byte_arr.getvalue()
                mpwriter.append(img_byte_arr, {
                    'Content-Type': 'image/jpeg'
                })
                await mpwriter.write(response, False)
            await asyncio.sleep(1/15)
        await response.drain()
    return response

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

    cam = db.get_camera(int(params['id']))
    player = MediaPlayer(cam.url, options={"rtsp_transport": "tcp"})#frameserver.get_player(cam.name)

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

async def addCamera(request):
    params = await request.json()
    cam = Camera(params['name'], params['url'])
    id = db.insert_camera(cam)
    cam.id = id
    db.update_camera(id, cam)
    asyncio.create_task(frameserver.capture(cam))
    return web.Response(status=201, text=json.dumps({'id': id}))

async def updateCamera(request):
    params = await request.json()
    cam = params['camera']
    old_cam = db.get_camera(cam['id'])
    if cam['name'] != old_cam.name and len(cam['name']) > 0:
        old_cam.name = cam['name']

    db.update_camera(cam['id'], old_cam)
    return web.Response(status=201)

async def getCameras(request):
    return web.Response(
        content_type="application/json",
        text=json.dumps(db.get_cameras(), default=lambda o: o.__dict__),
    )

async def deleteCamera(request):
    params = await request.json()
    db.delete_camera(int(params['id']))
    return web.Response(status=204)

async def getRecordings(request):
    return web.Response(
        content_type="application/json",
        text=json.dumps(os.listdir(db.get_settings().video_path), default=lambda o: o.__dict__),
    )

async def getRecording(request):
    name = request.match_info['name']
    path = db.get_settings().video_path + "/" + name
    return web.FileResponse(path)

async def getSettings(request):
    return web.Response(
        content_type="application/json",
        text=json.dumps(db.get_settings(), default=lambda o: o.__dict__),
    )

async def updateSettings(request):
    params = await request.json()
    settings = Settings(params['frameBufferSize'], params['videoPath'])
    db.update_settings(settings)
    return web.Response(status=201)

async def run(fs: FrameServer, database: DBConnector):
    global frameserver, db
    frameserver = fs
    db = database

    app = web.Application()
    app.router.add_get("/", multi)
    app.router.add_get("/test", test)
    app.router.add_get("/save", save)
    app.router.add_get("/streams/{id}", single)
    app.router.add_post("/webrtc/offer", offer)
    app.router.add_post("/camera", addCamera)
    app.router.add_put("/camera", updateCamera)
    app.router.add_delete("/camera", deleteCamera)
    app.router.add_get("/cameras", getCameras)
    app.router.add_get("/recordings", getRecordings)
    app.router.add_get("/recordings/{name}", getRecording)
    app.router.add_get("/settings", getSettings)
    app.router.add_put("/settings", updateSettings)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0' , 5000)
    await site.start()
