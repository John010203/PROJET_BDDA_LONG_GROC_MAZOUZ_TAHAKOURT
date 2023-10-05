
from CODE.DiskManager import DiskManager
from CODE.BufferManager import BufferManager
from CODE.DBParams import DBparams

class BDD:

    def __init__(self, DBParams):
        self.DBParams = DBParams
        self.disk_manager = DiskManager(self)
        self.buffer_manager = BufferManager(self)



dbb1 = BDD(DBparams(DBPath = "../DB",
                    SGBDPageSize = 4096,
                    DMFileCount = 4))

dbb2 = BDD(DBparams(DBPath = "../DB",
                    SGBDPageSize = 2048,
                    DMFileCount = 8))