
from DiskManager import DiskManager
from BufferManager import BufferManager
from DBParams import DBParams

class BDD:

    def __init__(self, DBParams):
        self.DBParams = DBParams
        self.disk_manager = DiskManager(self)
        #self.buffer_manager = BufferManager(self)
        

