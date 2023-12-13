import PageId
import ByteBuffer
from Frame import Frame

class BufferManager :

    def __init__(self, bdd):
        self.bdd = bdd
        self.disk_manager = bdd.disk_manager
        self.frameCount = bdd.DBParams.frameCount
        self.listFrame = [Frame() for i in range(self.frameCount)]
        
        
    def reset(self):
        #self.frameCount = 0
        for frame in self.listFrame :
            frame.clear()
             #a verifier
        
    def __str__(self):
        res = ""
        for i in range(len(self.listFrame)):
            res += "\n" +str(i)+ "\t" + str(self.listFrame[i])
        return res
    
    def FindFrameLibre(self)->int:
        index : int = None
        """
        LFU : 
        Une page peut être remplacée ssi son pin_count = 0
        • Choisir une frame parmi celles dont le contenu n'est pas utilisé couramment (pin_count=0) pour remplacer son contenu ;
        • Si la frame est marquée comme “dirty”, écrire d'abord son contenu sur le disque puis remettre son dirty à 0
        """
        #LFU
        #il ya une case libre
        for i in range(len(self.listFrame)) :
            if self.listFrame[i].page_id==None :
                #print("je suis nul. ca sera moi le prochain")
                index=i 
                return index 
        #on remplace
        min=None
        for i in range(len(self.listFrame)) :
            if self.listFrame[i].pin_count == 0:
                if min==None: #premier pincount a zero 
                    min=self.listFrame[i].LFU
                    index=i
                    
                else: 
                    if min>self.listFrame[i].LFU:
                        min=self.listFrame[i].LFU
                        index=i

                    
        if index==None : 
            raise Exception("Aucune frame disponible")
        # a verifier dans le cas d'une case vide
        if(self.listFrame[index].dirty):
            self.disk_manager.WritePage(self.listFrame[index].page_id,self.listFrame[index].buffer)

        self.listFrame[index].clear() 
        return index

    def FindFrame(self, pageId : PageId):#verifie si la page est deja chargee
        index = None
        for i in range(len(self.listFrame)) :
            if self.listFrame[i].page_id == pageId : 
                index = i 
        return index

    def GetPage(self, pageId : PageId) -> ByteBuffer:
        #print('debut frame 3',self.listFrame[2])
        if pageId.FileIdx == -1 and pageId.PageIdx == 0:
            return None

        indice = self.FindFrame(pageId) #La page est déjà chargé dans la frame
        if indice != None:
            self.listFrame[indice].pin_count+=1
            self.listFrame[indice].LFU+=1
            return self.listFrame[indice].buffer

        #La page n'est pas déjà chargé dans une frame
        i = self.FindFrameLibre()
        #print("indice frame libre",i)
        #print(self)
        
        frameId=self.listFrame[i]
        frameId.page_id = pageId
        self.bdd.disk_manager.ReadPage(pageId, frameId.buffer)
        frameId.pin_count+=1
        frameId.LFU+=1
        #print('fin frame 1 ',self.listFrame[0])
        #print('fin frame 2',self.listFrame[1])
        #print('fin frame 3',self.listFrame[2])
        return self.listFrame[i].buffer

    def FreePage(self, pageId : PageId, valdirty) -> None:
         """
         • Si la frame est marquée comme “dirty”, écrire d'abord son contenu sur le disque puis remettre son dirty à 0
         """
    
         for i in range(len(self.listFrame)) : 
                if self.listFrame[i].page_id == pageId :
                    #print("PAGE TROUVE ----------------")
                    self.listFrame[i].pin_count-=1
                    if valdirty:
                        self.listFrame[i].dirty = valdirty
                    self.listFrame[i].buffer.set_position(0)
                    if valdirty:
                        self.disk_manager.WritePage(pageId,self.listFrame[i].buffer)
             
                    #On a deja incremente le LFU dans GetPage
                
    
    def FlushAll(self) -> None :
        """
        ◦ l'écriture de toutes les pages dont le flag dirty = 1 sur disque
        ◦ la remise à 0 de tous les flags/informations et contenus des buffers (buffer pool « vide »)

        """
        for i in range(len(self.listFrame)):
            if(self.listFrame[i].dirty==1):
                self.bdd.disk_manager.WritePage(self.listFrame[i].page_id,self.listFrame[i].buffer)
            self.listFrame[i].clear()
