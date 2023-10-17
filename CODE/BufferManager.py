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
        #on peut regrouper les 2 conditions dans une seule boucle for
        #on n'est pas sense implementer LFU ici?
        """
        LFU : 
        Une page peut être remplacée ssi son pin_count = 0
        • Choisir une frame parmi celles dont le contenu n'est pas utilisé couramment (pin_count=0) pour remplacer son contenu ;
        • Si la frame est marquée comme “dirty”, écrire d'abord son contenu sur le disque puis remettre son dirty à 0
        """
        for i in range(len(self.listFrame)) :
            if self.listFrame[i].page_id==None :
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
            if self.listFrame[i].page_id == pageId : 
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
         #on n'est pas sense utiliser le flag dirty et valdirty?
         """
         • Si la frame est marquée comme “dirty”, écrire d'abord son contenu sur le disque puis remettre son dirty à 0
         """
         for i in range(len(self.listFrame)) : 
                if self.listFrame[i].pageId == pageId :
                    if self.listFrame[i].dirty == 1: 
                        self.listFrame[i].LFU=0
                else :
                    ""
    
    def FlushAll(self) -> None :
        """
        ◦ l'écriture de toutes les pages dont le flag dirty = 1 sur disque
        ◦ la remise à 0 de tous les flags/informations et contenus des buffers (buffer pool « vide »)

        """
        return
    

        
