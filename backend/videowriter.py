import av
from typing import List

class VideoWriter:
    def __init__(self, file) -> None:
        self.file = file

    def open(self):
        self.__output: av.OutputContainer = av.open(self.file, 'w')

    def write_packet(self, packet: av.Packet) -> None:
        if packet is None:
            return

        frames = packet.decode()
        vfs = [x for x in frames if isinstance(x, av.VideoFrame)]

        if (len(vfs) == 0):
            return 

        self.__try_add_stream(frames)
        self.__mux(vfs[0])

    def write_packets(self, packets: List[av.Packet]) -> None:
        if len(packets) == 0:
            return

        frames = [frames for frames in [frames.decode() for frames in packets] if len(frames) > 0]

        self.__try_add_stream(frames[0])

        for framelist in frames:
            #frame.pts = frame.pts
            #frame.time_base = frame.time_base
            self.__mux(framelist[0])
            

    def close(self):
        self.__output.close()

    def __try_add_stream(self, sample_frames: List[av.VideoFrame]):
        if len(self.__output.streams.video) == 0:
            self.__stream = self.__output.add_stream('libx264', '30')
            sample_frame = [x for x in sample_frames if isinstance(x, av.VideoFrame)][0]
            self.__stream.pix_fmt = sample_frame.format.name
            self.__stream.width = sample_frame.width
            self.__stream.height = sample_frame.height

    def __mux(self, frame: av.VideoFrame):
        print(frame)
        try:
            opacket = self.__stream.encode(frame)
        except Exception as e:
            print(e)
            return False

        if opacket is not None:
            try:
                self.__output.mux(opacket)
            except Exception:
                print('mux failed: ' + str(opacket))