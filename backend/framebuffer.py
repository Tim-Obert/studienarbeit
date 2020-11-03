import av
from typing import List

class FrameBuffer:
    def __init__(self, n):
        self.__buffer = [None for x in range(n)]
        self.__n = n
        self.__index = -1

    def __shift_to_sorted(self, buffer: list) -> list:
        l = buffer.copy()
        for i in range(self.__index + 1):
            l.append(l.pop(0))
        return l

    def add(self, item):
        if self.__index + 1 < self.__n:
            self.__index += 1
        else:
            self.__index = 0
        self.__buffer[self.__index] = item

    def get_frames(self) -> List[av.VideoFrame]:
        return self.__shift_to_sorted(self.__buffer)

    def get_latest_frame(self) -> av.VideoFrame:
        return self.__buffer[self.__index]

    def get_index(self) -> int:
        return self.__index

