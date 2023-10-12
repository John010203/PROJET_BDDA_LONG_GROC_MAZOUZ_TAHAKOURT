import PageId
import ByteBuffer
from Frame import Frame

class BufferManager :

    def __init__(self, bdd):
        self.bdd = bdd
        self.disk_manager = bdd.disk_manager
        self.frameCount = bdd.DBParams.frameCount
        self.listFrame : list = [Frame()]*self.frameCount

    def FindFrameLibre(self):
        index : int = None
        for i in range(len(self.listFrame)) :
            if self.listFrame[i].pageId==None :
                index=i
        for i in range(len(self.listFrame)) :
            if self.listFrame[i].pin_count == 0:  
                index = i
        if index==None : 
            raise Exception("Aucune frame disponible")
        return index

    def FindFrame(self, pageId : PageId):#verifie si la page est deja chargee
        index = None
        for i in range(len(self.listFrame)) :
            if self.listFrame[i].pageId == pageId : 
                index = i 
        return index

    def GetPage(self, pageId : PageId) -> ByteBuffer:
        indice = self.FindFrame(pageId) #La page est déjà chargé dans la frame
        if indice != None:
            self.listFrame[indice].pin_count+=1
            self.listFrame[indice].LFU+=1
            return self.listFrame[indice].buffer

        #La page n'est pas déjà chargé dans une frame
        i = self.FindFrameLibre()
        
        frameId=self.listFrame[i]
        frameId.page_id = pageId
        self.bdd.disk_manager.ReadPage(pageId, frameId.buffer)
        frameId.pin_count+=1
        frameId.LFU+=1
        return self.listFrame[i].buffer

    def FreePage(self, pageId : PageId, valdirty : int | bool) -> None:
         for i in range(len(self.listFrame)) : 
                if self.listFrame[i].pageId == pageId :
                    if self.listFrame[i].dirty == 1: 
                        self.listFrame[i].LFU=0
                else :
                    ""
    
    def FlushAll(self) -> None :
        return
    

        
