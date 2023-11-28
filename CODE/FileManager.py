from PageId import PageId
from HeaderPage import HeaderPage
from DataPage import DataPage
from RecordId import RecordId


class FileManager:
    def __init__(self, bdd) -> None:
        self.bdd=bdd

    def createNewHeaderPage(self)->PageId:
        pageId = self.bdd.disk_manager.AllocPage()
        frameBuffer = self.bdd.buffer_manager.getPage()
        headerPage = HeaderPage(frameBuffer)
        headerPage.setFreePageId(PageId(-1,0))
        headerPage.setFullPageId(PageId(-1,0))
        self.bdd.buffer_manager.FreePage(pageId,True)
        return pageId
    
    def addDataPage(self,tabInfo)->PageId:
        #charger notre headerPage en RAM
        pageIdHeader= tabInfo.headerPageId
        headerPageBuff=self.bdd.buffer_manager.getPage(pageIdHeader)
        headerPage=HeaderPage(headerPageBuff)

        #Faire la meme chose avec notre data page
        pageIdData=self.bdd.disk_manager.AllocPage()
        dataPageBuff=self.bdd.buffer_manager.getPage(pageIdData)
        dataPage = DataPage(dataPageBuff)

        #on fait le chainage
        dataPage.setPageId(headerPage.getFreePageId())
        headerPage.setFreePageId(pageIdData)

        self.bdd.buffer_manager.FreePage(pageIdHeader,True)
        self.bdd.buffer_manager.FreePage(pageIdData,True)
        return pageIdData
    
    
    def getFreeDataPageId(self,tabInfo,sizeRecord)->PageId:
        headerBuffer = self.bdd.buffer_manager.GetPage(tabInfo.headerPageId) #on charge juste le buffer dans lequel on va ecrire
        headerPage = HeaderPage(headerBuffer)
        pageId = headerPage.getFreePageId()
        self.bdd.buffer_manager.FreePage(pageId,False)
        pageBuffer = self.bdd.buffer_manager.GetPage(pageId) #on charge juste le buffer dans lequel on va ecrire
        dataPage = DataPage(pageBuffer)
        while not(pageId.FileIdx == -1 and pageId.PageIdx == 0) and sizeRecord > dataPage.getEspaceDisponible():
            pageId = dataPage.nextPageId()
            pageBuffer = self.bdd.buffer_manager.GetPage(pageId) #on charge juste le buffer dans lequel on va ecrire
            dataPage = DataPage(pageBuffer)

        return pageId
    
    def writeRecordToDataPage(self,record,pageId)->RecordId:
        return


        

