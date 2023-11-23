from PageId import PageId
from DiskManager import DiskManager

class FileManager:
    def __init__(self, bdd) -> None:
        self.bdd=bdd;

    def createNewHeaderPage(self)->PageId:
        pageId = self.bdd.disk_manager.AllocPage()
        frameBuffer = self.bdd.buffer_manager.getPage();
        frameBuffer.put_int(-1)
        frameBuffer.put_int(0)
        frameBuffer.put_int(-1)
        frameBuffer.put_int(0)
    

        

