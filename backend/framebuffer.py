import av
from typing import List
import rx
from rx.core.typing import Observable, Observer

class FrameBuffer:
    def __init__(self, n):
        self.__buffer = [None for x in range(n)]
        self.__n = n
        self.__index = -1
        self.__observer: Observer = None
    
        def frame_observer(observer, scheduler):
            self.__observer = observer

        self.__observable: Observable = rx.create(frame_observer)

    def __shift_to_sorted(self, buffer: list) -> list:
        l = buffer.copy()
        for i in range(self.__index + 1):
            l.append(l.pop(0))
        return l

    def add(self, item: av.Packet):
        if self.__index + 1 < self.__n:
            self.__index += 1
        else:
            self.__index = 0
        self.__buffer[self.__index] = item
        if self.__observer is not None:
            self.__observer.on_next(item)

    def get_packets(self) -> List[av.Packet]:
        return [packet for packet in self.__shift_to_sorted(self.__buffer) if packet is not None]

    def get_latest_packet(self) -> av.Packet:
        return self.__buffer[self.__index]

    def get_latest_keyframe(self) -> av.Packet:
        keyframes = [x for x in self.__shift_to_sorted(self.__buffer) if x is not None and x.is_keyframe]
        if (len(keyframes) > 0):
            return keyframes[-1]
        else:
            return None

    def get_index(self) -> int:
        return self.__index

    def get_observable(self) -> Observable[av.VideoFrame]:
        return self.__observable

