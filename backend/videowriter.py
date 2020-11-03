import av
from typing import List

class VideoWriter:
    def __init__(self, file) -> None:
        self.file = file

    def write(self, frames: List[av.VideoFrame]) -> None:
        print("writing " + len(frames) + " frames to file")
        frames = [frame for frame in frames if frame is not None]
        output = av.open(self.file, 'w')
        stream = output.add_stream('libx264', '30')
        stream.pix_fmt = frames[0].format.name
        stream.width = frames[0].width
        stream.height = frames[0].height

        for frame in frames:
            frame.pts = frame.pts
            frame.time_base = frame.time_base
            
            try:
                opacket = stream.encode(frame)
            except Exception:
                return False

            if opacket is not None:
                try:
                    output.mux(opacket)
                except Exception:
                    print('mux failed: ' + str(opacket))

        output.close()