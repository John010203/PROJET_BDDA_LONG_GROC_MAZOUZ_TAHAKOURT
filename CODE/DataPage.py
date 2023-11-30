from PageId import PageId
class DataPage : 
    def __init__(self,buff):
        #buff devra contenir les PageId et les donnees
        self.buff = buff

    def setPageId(self,pageId):
        self.buff.set_position(0)
        self.buff.put_int(pageId.FileIdx)
        self.buff.put_int(pageId.PageIdx)

    def nextPageId(self):
        self.buff.set_position(0)
        pageId = PageId(self.buff.read_int(),self.buff.read_int())
        return pageId

    def getPosition(): return
    def setPosition(pos):return
    def getRecordAt(pos):return 
    def getEspaceDisponible(self):
        self.buff.set_position(4096-8)
        nbSlot = self.buff.read_int()
        posFreeArea = self.buff.read_int()
        return 4096-(nbSlot*8)-posFreeArea-8