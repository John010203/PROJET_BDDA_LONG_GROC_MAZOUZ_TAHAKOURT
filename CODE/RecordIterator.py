from PageId import PageId
from TableInfo import TableInfo
from BufferManager import BufferManager
from DataPage import DataPage
from Record import Record

class RecordIterator:
    def __init__(self,bdd,tabInfo,pageId):
        self.bdd=bdd
        self.buffer_manager=self.bdd.buffer_manager
        self.tabInfo=tabInfo
        self.pageId=pageId
        self.buffRI=self.buffer_manager.GetPage(self.pageId)
        self.dataPage=DataPage(self.buffRI)
        self.dataPage.setBufferAt(8) #position du premier record.

    def GetNextRecord(self,index)->Record: #index correspond a l'index de la boucle sur laquelle on va iterer
        print("self.buffRI.get_pos() : ",self.buffRI.get_pos())
        valSlot= self.dataPage.getValeurSlotAt(index,self.bdd,self.buffRI.get_pos())
        record=Record(self.tabInfo,[])
        taille=record.readFromBuffer(self.buffRI,self.buffRI.get_pos())
        #self.buffRI.set_position(self.buffRI.get_pos()+taille+4*len(self.tabInfo.cols))
        if(valSlot!=-1 or record.getTailleRecord() != 0):
            print("record : ", record.getTailleRecord())
            return record
        else:
            return None
    
    def Close(self):
        self.buffer_manager.FreePage(self.pageId,False)

    def Reset(self):
        self.dataPage.setBufferAt(8)

