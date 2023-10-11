import PageId
import ByteBuffer
from Buffer import Buffer

class BufferManager :

    def __init__(self, bdd):
        self.bdd = bdd
        self.disk_manager = bdd.disk_manager

    def GetPage(self, pageId : PageId) -> Buffer:
        return 

    def FreePage(self, pageId : PageId, valdirty : int | bool) -> None:
        return 
    
    def FlushAll(self) -> None :
        return
    

        
