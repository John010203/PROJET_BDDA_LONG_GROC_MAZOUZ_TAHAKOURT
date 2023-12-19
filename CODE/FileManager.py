from PageId import PageId
from HeaderPage import HeaderPage
from DataPage import DataPage
from RecordId import RecordId
from Record import Record

class FileManager:
    def __init__(self, bdd) -> None:
        """
        Initialise une instance de la classe FileManager
        """
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
        print('zhat',pageId)
        headerPage.buff.set_position(0)
        self.bdd.buffer_manager.FreePage(pageId,True)
        return pageId
    
    def addDataPage(self,tabInfo)->PageId:
        """
        Ajoute un nouveau PageId dans la table
        """
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
        """
        Récupère le PageId du premier PageId libre pouvant contenir le record
        """
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
        """
        Ecrit un record dans une page
        """
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
        """
        Récupère les records d'une page
        """
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
        """
        Récupère la liste des pages
        """
        headerPageId=tabInfo.headerPageId
        buffHeaderPage=self.bdd.buffer_manager.GetPage(headerPageId)
        headerPage=HeaderPage(buffHeaderPage,self.bdd)

        listePagesFree = headerPage.getPagesFromListe(headerPage.getFreePageId())
        
        fullPageId = headerPage.getFullPageId()
        self.bdd.buffer_manager.FreePage(headerPageId,False)
        #print('aaaaaaaaaaaaaaaaaaaaaaaaaaaa3hhhhhhhhhhhh',headerPageId,fullPageId)
        listePagesFull = []
        
        if(fullPageId.FileIdx != -1):
            listePagesFull=headerPage.getPagesFromListe(headerPage.getFullPageId())
        return listePagesFree + listePagesFull
    
    def InsertRecordIntoTable(self, record):
        """
        Insère un record dans la table
        """
        getFree = self.getFreeDataPageId(record.tabInfo,record.getTailleRecord())
        
        freeDataPage = None
        if getFree!=None :
            freeDataPage =  getFree
        else : 
            freeDataPage = self.addDataPage(record.tabInfo)  
   
        return self.writeRecordToDataPage(record,freeDataPage)

    
    def GetAllRecords(self,tabInfo):
        """
        Récupère tous les records de la table
        """
        listePages=self.getDataPages(tabInfo)
        res = []
        
        for p in listePages :
            if p.FileIdx !=-1:
                res += self.getRecordsInDataPage(tabInfo,p)
        return res