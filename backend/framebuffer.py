class FrameBuffer:
    def __init__(self, n):
        self.__buffer = [None for x in range(n)]
        self.__n = n
        self.__index = -1

    def add(self, item):
        if self.__index + 1 < self.__n:
            self.__index += 1
        else:
            self.__index = 0
        self.__buffer[self.__index] = item

    def get_buffer(self) -> list:
        return self.__shift_to_sorted(self.__buffer)

    def get_index(self) -> int:
        return self.__index

    def __shift_to_sorted(self, buffer: list) -> list:
        l = buffer.copy()
        for i in range(self.__index + 1):
            l.append(l.pop(0))
        return l

