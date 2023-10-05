import PageId
import ByteBuffer

class BufferManager :

    def __init__(self, bdd):
        self.bdd = bdd
        self.disk_manager = bdd.disk_manager


        
