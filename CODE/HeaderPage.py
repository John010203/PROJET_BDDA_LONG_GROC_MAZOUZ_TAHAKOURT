from PageId import PageId
class HeaderPage : 
    def __init__(self,buff):
        self.buff = buff
        dirty = False

    def setFreePageId (self,pageId:PageId): #DES QUIL YA UN SET ON MET LE DIRTY A TRUE
        dirty=True
        self.buff.set_position(0)
        self.buff.put_int(pageId.FileIdx)
        self.buff.put_int(pageId.PageIdx)

    def setFullPageId (self,pageId:PageId): #DES QUIL YA UN SET ON MET LE DIRTY A TRUE
        dirty=True
        self.buff.set_position(8)
        self.buff.put_int(pageId.FileIdx)
        self.buff.put_int(pageId.PageIdx)
        return 
    
    def getFreePageId (self)->PageId:
        self.buff.set_position(0)
        fileId=self.buff.read_int()
        pageId=self.buff.read_int()
        return PageId(fileId,pageId)

    def getFullPageId (self)->PageId:
        self.buff.set_position(8)
        fileId=self.buff.read_int()
        pageId=self.buff.read_int()
        return PageId(fileId,pageId)
