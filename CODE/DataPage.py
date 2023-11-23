class DataPage : 
    def __init__(self,buff):
        #buff devra contenir les PageId et les donnees
        self.buff = buff

    def setPageId(self,pageId):
        self.buff.set_position(0)
        self.buff.put_int(pageId.FileIdx)
        self.buff.put_int(pageId.PageIdx)

    def getPosition(): return
    def setPosition(pos):return
    def getRecordAt(pos):return 
    def getEspaceDisponible():return