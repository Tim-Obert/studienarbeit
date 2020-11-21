import av
from typing import List

class VideoWriter:
    def __init__(self, file) -> None:
        self.file = file

    def open(self):
        self.__output: av.OutputContainer = av.open(self.file, 'w')

    def write_frame(self, frame: av.VideoFrame) -> None:
        print("writing 1 frame to file")
        if frame is None:
            return

        self.__try_add_stream(frame)
        self.__mux(frame)

    def write_frames(self, frames: List[av.VideoFrame]) -> None:
        print("writing " + str(len(frames)) + " frames to file")
        frames = [frame for frame in frames if frame is not None]

        self.__try_add_stream(frames[0])

        for frame in frames:
            #frame.pts = frame.pts
            #frame.time_base = frame.time_base
            self.__mux(frame)
            

    def close(self):
        self.__output.close()

    def __try_add_stream(self, sample_frame: av.VideoFrame):
        if len(self.__output.streams.video) == 0:
            self.__stream = self.__output.add_stream('libx264', '30')
            self.__stream.pix_fmt = sample_frame.format.name
            self.__stream.width = sample_frame.width
            self.__stream.height = sample_frame.height

    def __mux(self, frame: av.VideoFrame):
        try:
            opacket = self.__stream.encode(frame)
        except Exception:
            return False

        if opacket is not None:
            try:
                self.__output.mux(opacket)
            except Exception:
                print('mux failed: ' + str(opacket))