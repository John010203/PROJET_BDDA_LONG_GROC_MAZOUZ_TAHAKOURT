from PageId import PageId
from DataPage import DataPage
class HeaderPage : 
    def __init__(self,buff,bdd):
        self.bdd = bdd
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
    
    def getPagesFromListe(self,pageId):
        listePage= []
        listePage.append(pageId)
        
        if pageId.FileIdx != -1 :
            buffPage=self.bdd.buffer_manager.GetPage(pageId)
            dataPage= DataPage(buffPage)
            nextPage= dataPage.nextPageId()
            self.bdd.buffer_manager.FreePage(pageId,False)
            listePage = listePage + [nextPage]
            while(nextPage.FileIdx!=-1):
                buffPage=self.bdd.buffer_manager.GetPage(nextPage)
                dataPage= DataPage(buffPage)
                nextPage = dataPage.nextPageId()
                if nextPage.FileIdx !=-1:
                    self.bdd.buffer_manager.FreePage(nextPage,False)
                listePage = listePage + [nextPage]
            self.bdd.buffer_manager.FreePage(nextPage,False)
        return listePage



