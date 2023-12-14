from PageId import PageId
from HeaderPage import HeaderPage
from DataPage import DataPage
from RecordId import RecordId
from Record import Record

class FileManager:
    def __init__(self, bdd) -> None:
        self.bdd=bdd

    def createNewHeaderPage(self)->PageId:
        '''
        Cree un nouveau headerPage insere (-1,0) et le premier pageId de notre table
        '''
        pageId = self.bdd.disk_manager.AllocPage()
        frameBuffer = self.bdd.buffer_manager.GetPage(pageId)
        headerPage = HeaderPage(frameBuffer,self.bdd)
        headerPage.setFreePageId(PageId(-1,0))
        headerPage.setFullPageId(PageId(-1,0))
        headerPage.buff.set_position(0)
        self.bdd.buffer_manager.FreePage(pageId,True)
        return pageId
    
    def addDataPage(self,tabInfo)->PageId:
        #charger notre headerPage en RAM
        pageIdHeader= tabInfo.headerPageId

        headerPageBuff=self.bdd.buffer_manager.GetPage(pageIdHeader)

        headerPage=HeaderPage(headerPageBuff,self.bdd)
        #Faire la meme chose avec notre data page
        #on harge une nouvelle page
        pageIdData=self.bdd.disk_manager.AllocPage()
        #on recup son buffer
        dataPageBuff=self.bdd.buffer_manager.GetPage(pageIdData)
        dataPage = DataPage(dataPageBuff)
        #on initialise son buffer
        dataPage.initialisation()

        dataPage.buff.set_position(0)
       
        #on fait le chainage
        dataPage.setPageId(headerPage.getFreePageId())
        dataPageBuff.set_position(0)
        headerPage.setFreePageId(pageIdData)

        self.bdd.buffer_manager.FreePage(pageIdHeader,True)
        self.bdd.buffer_manager.FreePage(pageIdData,True)
        return pageIdData
    
    
    def getFreeDataPageId(self,tabInfo,sizeRecord)->PageId:
        headerBuffer = self.bdd.buffer_manager.GetPage(tabInfo.headerPageId) #on charge juste le buffer dans lequel on va ecrire
        headerPage = HeaderPage(headerBuffer,self.bdd)
        #premiere page libre de la liste chainee
        pageId = headerPage.getFreePageId()
        self.bdd.buffer_manager.FreePage(tabInfo.headerPageId,False)

        while not(pageId.FileIdx == -1):

            pageBuffer = self.bdd.buffer_manager.GetPage(pageId) #on charge juste le buffer dans lequel on va ecrire
            dataPage = DataPage(pageBuffer)      
            if sizeRecord > dataPage.getEspaceDisponible():  

                pageIdPrev=pageId
                pageId = dataPage.nextPageId()
                self.bdd.buffer_manager.FreePage(pageIdPrev,False)

            else:
                self.bdd.buffer_manager.FreePage(pageId,False)
                return pageId
        return  None
    
    
    def writeRecordToDataPage(self,record,pageId)->RecordId: 
        buffPage = self.bdd.buffer_manager.GetPage(pageId)
        dataPage = DataPage(buffPage)
       
        nbSlots = dataPage.getNbSlots(self.bdd)

        debutEspaceDispo = dataPage.getdebutEspaceDispo(self.bdd)

        tailleRecord=record.getTailleRecord()

        dataPage.putNewSlot(self.bdd,tailleRecord)

        record.writeToBuffer(buffPage,debutEspaceDispo)

        nbSlots+=1
        dataPage.setNbSlots(nbSlots,self.bdd)

        debutEspaceDispo+=tailleRecord
        dataPage.setdebutEspaceDispo(debutEspaceDispo,self.bdd)

        self.bdd.buffer_manager.FreePage(pageId,True)

        return RecordId(pageId,nbSlots)
    
    def getRecordsInDataPage(self,tabInfo,pageId):
        print('pageId datapage ', pageId)
        buffPage=self.bdd.buffer_manager.GetPage(pageId)
        dataPage = DataPage(buffPage)

        nbSlots= dataPage.getNbSlots(self.bdd)
        buffPage.set_position(8)
        listeRecords=[]
        for i in range(0,nbSlots):
            pos=buffPage.get_pos()

            record=Record(tabInfo,[])
            taille=record.readFromBuffer(buffPage,pos)

            listeRecords.append(record)
            buffPage.set_position(pos+taille+4*len(tabInfo.cols))
        
        self.bdd.buffer_manager.FreePage(pageId,False)
        return listeRecords
    
    
    def getDataPages(self,tabInfo):

        headerPageId=tabInfo.headerPageId
        buffHeaderPage=self.bdd.buffer_manager.GetPage(headerPageId)
        headerPage=HeaderPage(buffHeaderPage,self.bdd)
        self.bdd.buffer_manager.FreePage(headerPageId,False)

        listePagesFree = headerPage.getPagesFromListe(headerPage.getFreePageId())
        fullPageId = headerPage.getFullPageId()
        listePagesFull = []
        if(fullPageId.FileIdx != -1):
            listePagesFull=headerPage.getPagesFromListe(headerPage.getFullPageId())
        print('listes free et full :',listePagesFree + listePagesFull)
        return listePagesFree + listePagesFull
    
    def InsertRecordIntoTable(self, record):
        getFree = self.getFreeDataPageId(record.tabInfo,record.getTailleRecord())
        
        freeDataPage = None
        if getFree!=None :
            freeDataPage =  getFree
        else : 
            freeDataPage = self.addDataPage(record.tabInfo)  
   
        return self.writeRecordToDataPage(record,freeDataPage)

    
    def GetAllRecords(self,tabInfo):
        listePages=self.getDataPages(tabInfo)
        res = []
        print(listePages)
        for p in listePages :
            res += self.getRecordsInDataPage(tabInfo,p)
        return [t.__str__() for t in res]