class Buffer :
    def __init__(self) -> None:
        self.donnée = None
        self.page_id = None
        self.dirty = False
        self.pin_count = 0
        #self.LFU = 0