from ByteBuffer import ByteBuffer

class Frame :
    def __init__(self) -> None:
        self.buffer : ByteBuffer = ByteBuffer()
        self.page_id = None
        self.dirty = False
        self.pin_count = 0
        self.LFU = 0

    def clear(self):
        return 
    