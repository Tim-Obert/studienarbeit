from frameserver import FrameServer
from cameraregistry import CameraRegistry
from flask import Flask, render_template

app = Flask(__name__)

fs = None

@app.route('/')
def multi():
    return render_template("multi.html")


@app.route("/<name>")
def single(name):
    return "<img src='data:image/jpeg;base64," + fs.get_frame_jpeg(name) + "'/>"

def start(x: FrameServer):
    global fs
    fs = x

    app.run()