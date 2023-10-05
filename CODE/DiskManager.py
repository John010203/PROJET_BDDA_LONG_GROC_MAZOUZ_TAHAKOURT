import PageId
import ByteBuffer

class DiskManager :

    def __init__(self, bdd):
        self.bdd = bdd

        self.fileCounter = [0]*4

        self.pagesDisponibles = []


    def AllocPage(self) -> PageId :
        if (len(self.pagesDisponibles)!=0):
            return self.pagesDisponibles.pop(0)
        else:
            index = self.fileCounter.index(min(self.fileCounter))
            self.fileCounter[index]+=1
            return PageId(index, self.fileCounter[index])

    def ReadPage(self,pageId: PageId, buff : ByteBuffer) -> None:
        return
    
    def WritePage(self,pageId: PageId, buff) -> None:
        return

    def Dealloc(self,pageId:PageId) -> None: 
        self.pagesDisponibles.append(pageId)
        self.pagesUtilisees.pop(pageId)

    def GetCurrentCountAllocPages(self) ->  int :
        """Retourne le nombre de pages allouées"""
        return len(self.pagesUtilisees)