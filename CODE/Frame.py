from ByteBuffer import ByteBuffer

class Frame :
    def __init__(self) -> None:
        self.buffer : ByteBuffer = ByteBuffer()
        self.page_id = None
        self.dirty = False
        self.pin_count = 0
        self.LFU = 0

    def clear(self):
        self.page_id = None
        self.dirty = False
        self.pin_count = 0
        self.LFU = 0
        
    def __str__(self):
        return " PAGEID : "+ str(self.page_id) + " DIRTY " +str(self.dirty) + " PINCOUNT " + str(self.pin_count)
