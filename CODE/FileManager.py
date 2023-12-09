from PageId import PageId
from HeaderPage import HeaderPage
from DataPage import DataPage
from RecordId import RecordId
from Record import Record

class FileManager:
    def __init__(self, bdd) -> None:
        self.bdd=bdd

    def createNewHeaderPage(self)->PageId:
        pageId = self.bdd.disk_manager.AllocPage()
        frameBuffer = self.bdd.buffer_manager.GetPage(pageId)
        headerPage = HeaderPage(frameBuffer)
        headerPage.setFreePageId(PageId(-1,0))
        headerPage.setFullPageId(PageId(-1,0))
        self.bdd.buffer_manager.FreePage(pageId,True)
        return pageId
    
    def addDataPage(self,tabInfo)->PageId:
        #charger notre headerPage en RAM
        pageIdHeader= tabInfo.headerPageId
        headerPageBuff=self.bdd.buffer_manager.GetPage(pageIdHeader)
        headerPage=HeaderPage(headerPageBuff)
        #Faire la meme chose avec notre data page
        pageIdData=self.bdd.disk_manager.AllocPage()
        dataPageBuff=self.bdd.buffer_manager.GetPage(pageIdData)
        dataPage = DataPage(dataPageBuff)
        dataPage.initialisation()
        #on fait le chainage
        dataPage.setPageId(headerPage.getFreePageId())
        dataPageBuff.set_position(0)
        headerPage.setFreePageId(pageIdData)
        self.bdd.buffer_manager.FreePage(pageIdHeader,True)
        self.bdd.buffer_manager.FreePage(pageIdData,True)
        self.bdd.disk_manager.WritePage(pageIdData,dataPageBuff)

        return pageIdData
    
    
    def getFreeDataPageId(self,tabInfo,sizeRecord)->PageId:
        headerBuffer = self.bdd.buffer_manager.GetPage(tabInfo.headerPageId) #on charge juste le buffer dans lequel on va ecrire
        headerPage = HeaderPage(headerBuffer)
        pageId = headerPage.getFreePageId()
        print(pageId)
        pageBuffer = self.bdd.buffer_manager.GetPage(pageId) #on charge juste le buffer dans lequel on va ecrire
        pageBuffer.set_position(0)
        print('--la--'+str(pageBuffer.read_int()))
        dataPage = DataPage(pageBuffer)  
        self.bdd.buffer_manager.FreePage(tabInfo.headerPageId,False)
        
        while not(pageId.FileIdx == -1) and sizeRecord > dataPage.getEspaceDisponible():
            print(dataPage.getEspaceDisponible())
            pageId = dataPage.nextPageId()
            print('--ici-'+str(pageId))
            pageBuffer = self.bdd.buffer_manager.GetPage(pageId) #on charge juste le buffer dans lequel on va ecrire
            dataPage = DataPage(pageBuffer)
            self.bdd.buffer_manager.FreePage(pageId,False)

        
        return pageId if pageId.FileIdx!=-1 else None
    
    def writeRecordToDataPage(self,record,pageId)->RecordId:
        buffPage = self.bdd.buffer_manager.GetPage(pageId)
        buffPage.set_position(self.bdd.DBParams.SGBDPageSize-8)
        nbSlots= buffPage.read_int()
        #print(nbSlots)
        debutEspaceDispo=buffPage.read_int()
        tailleRecord=record.getTailleRecord()
        buffPage.set_position(self.bdd.DBParams.SGBDPageSize-16-(nbSlots*8)) #le -16 pour pas ecrase les deux derniers entiers
        buffPage.put_int(debutEspaceDispo)
        buffPage.put_int(tailleRecord)
        buffPage.set_position(debutEspaceDispo)
        record.writeToBuffer(buffPage,buffPage.get_pos())
        buffPage.set_position(self.bdd.DBParams.SGBDPageSize-8)
        nbSlots+=1
        buffPage.put_int(nbSlots)
        debutEspaceDispo+=tailleRecord
        buffPage.put_int(debutEspaceDispo)
        self.bdd.buffer_manager.FreePage(pageId,True)
        return RecordId(pageId,nbSlots)
    
    def getRecordsInDataPage(self,tabInfo,pageId):
        buffPage=self.bdd.buffer_manager.GetPage(pageId)
        buffPage.set_position(self.bdd.DBParams.SGBDPageSize-8)
        nbSlots= buffPage.read_int()
        buffPage.set_position(8)
        listeRecords=[]
        for i in range(0,nbSlots):
            pos=buffPage.get_pos()
            record=Record(tabInfo,[])
            taille=record.readFromBuffer(buffPage,pos)
            listeRecords.append(record)
            buffPage.set_position(pos+taille)
        
        self.bdd.buffer_manager.FreePage(pageId,False)
        return listeRecords
    
    
    def getDataPages(self,tabInfo):
        headerPageId=tabInfo.headerPageId
        buffHeaderPage=self.bdd.buffer_manager.GetPage(headerPageId)
        headerPage=HeaderPage(buffHeaderPage)
        self.bdd.buffer_manager.FreePage(headerPageId)
        listePagesFree= headerPage.getPagesFromListe(headerPage.getFreePageId)
        listePagesFull=headerPage.getPagesFromListe(headerPage.getFullPageId)
        return listePagesFree+listePagesFull
    
    def InsertRecordIntoTable(self, record):
        freeDataPage=self.getFreeDataPageId(record.tabInfo,record.getTaille())
        return self.writeRecordToDataPage(record,freeDataPage)
    
    def GetAllRecords(self,tabInfo):
        listePages=self.getDataPages(tabInfo)
        return [self.getRecordsInDataPage(tabInfo,p) for p in listePages]