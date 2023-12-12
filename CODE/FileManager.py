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
        headerPage = HeaderPage(frameBuffer)
        headerPage.setFreePageId(PageId(-1,0))
        headerPage.setFullPageId(PageId(-1,0))
        headerPage.buff.set_position(0)
        #print("ICI",headerPage.buff.read_int(),headerPage.buff.read_int())
        #print("ICI",headerPage.buff.read_int(),headerPage.buff.read_int())
        #print("ICI",headerPage.buff.read_int(),headerPage.buff.read_int())
        self.bdd.buffer_manager.FreePage(pageId,True)
        return pageId
    
    def addDataPage(self,tabInfo)->PageId:
        #charger notre headerPage en RAM
        pageIdHeader= tabInfo.headerPageId
        #print("1 :",pageIdHeader)

        headerPageBuff=self.bdd.buffer_manager.GetPage(pageIdHeader)
        #print("2 : ",headerPageBuff.read_int(),headerPageBuff.read_int())

        headerPage=HeaderPage(headerPageBuff)
        #Faire la meme chose avec notre data page
        #on harge une nouvelle page
        pageIdData=self.bdd.disk_manager.AllocPage()
        #print("3 :",pageIdData)
        #on recup son buffer
        print('---------------dans dataOage-------------',pageIdData)
        print(self.bdd.buffer_manager)
        dataPageBuff=self.bdd.buffer_manager.GetPage(pageIdData)
        dataPage = DataPage(dataPageBuff)
        #on initialise son buffer
        dataPage.initialisation()

        dataPage.buff.set_position(0)
        #print("4 : ",dataPage.buff.read_int(),dataPage.buff.read_int())
       
        #on fait le chainage
        dataPage.setPageId(headerPage.getFreePageId())
        #print("5 : header page free pageid : ",dataPage.buff.read_int(),dataPage.buff.read_int())
        dataPageBuff.set_position(0)
        headerPage.setFreePageId(pageIdData)
        #headerPage.buff.set_position(0)
        #print("6 : prochaine page : ",headerPage.buff.read_int(),headerPage.buff.read_int())
        self.bdd.buffer_manager.FreePage(pageIdHeader,True)
        self.bdd.buffer_manager.FreePage(pageIdData,True)
        #print('#########',pageIdData)
        return pageIdData
    
    
    def getFreeDataPageId(self,tabInfo,sizeRecord)->PageId:
        headerBuffer = self.bdd.buffer_manager.GetPage(tabInfo.headerPageId) #on charge juste le buffer dans lequel on va ecrire
        headerPage = HeaderPage(headerBuffer)
        #premiere page libre de la liste chainee
        pageId = headerPage.getFreePageId()
        print('1:',pageId)
        pageBuffer = self.bdd.buffer_manager.GetPage(pageId) #on charge juste le buffer dans lequel on va ecrire

        dataPage = DataPage(pageBuffer)  
        self.bdd.buffer_manager.FreePage(tabInfo.headerPageId,False)
        
        while not(pageId.FileIdx == -1):
            if sizeRecord > dataPage.getEspaceDisponible():  
                print("page libre de la liste chainee",pageId)
                print("espace libre dans cette page",dataPage.getEspaceDisponible())
                pageIdPrev=pageId
                pageId = dataPage.nextPageId()
                print('Next PageId',pageId)
                if(pageId.FileIdx!=-1):
                    print("PAS ENCORE ARRIVEE A LA FIN",pageId)
                    buff = self.bdd.buffer_manager.GetPage(pageId) 
                    buff.set_position(4088)
                    print('----------------',pageId,buff.read_int(),buff.read_int())
                    #ici notre data age contient -1 0
                    dataPage = DataPage(buff)
                    print(dataPage.getEspaceDisponible())
                    self.bdd.buffer_manager.FreePage(pageIdPrev,False)
                else:
                    #a verifier
                    self.bdd.buffer_manager.FreePage(pageIdPrev,False)
                    self.bdd.buffer_manager.FreePage(pageId,False)
                    print("Vous n'avez plus d'espace.")
                    return self.addDataPage(tabInfo)
                    
            else:
                self.bdd.buffer_manager.FreePage(pageId,False)
                return pageId

        
        return pageId if pageId.FileIdx!=-1 else None
    
    def writeRecordToDataPage(self,record,pageId)->RecordId:
        buffPage = self.bdd.buffer_manager.GetPage(pageId)
        buffPage.set_position(self.bdd.DBParams.SGBDPageSize-8)
        nbSlots= buffPage.read_int()
        #print('ici nb slots+pageId avant ecriture ',pageId,nbSlots)
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
        #buffPage.set_position(self.bdd.DBParams.SGBDPageSize-8)
        #print("nbSlots dans writeRecordToBuffer",buffPage.read_int())
        debutEspaceDispo+=tailleRecord
        buffPage.put_int(debutEspaceDispo)
        self.bdd.buffer_manager.FreePage(pageId,True)
        #buffPage.set_position(self.bdd.DBParams.SGBDPageSize-8)
        #nbSlots= buffPage.read_int()
        #print('ici nb slots+pageId apres ecriture ',pageId,nbSlots)
        return RecordId(pageId,nbSlots)
    
    def getRecordsInDataPage(self,tabInfo,pageId):
        buffPage=self.bdd.buffer_manager.GetPage(pageId)
        #print("Dans la fonction",buffPage)
        #buffPage.set_position(0)
        #-1 0 est bien ecrit ya juste le nbSlots qui n'est pas ecrit
        #print("1:",pageId,buffPage.read_int(),buffPage.read_int())
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