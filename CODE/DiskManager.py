import PageId
import ByteBuffer

class DiskManager :

    diskManager = DiskManager()

    def __init__(self):
        self.pagesDisponibles = []
        self.pagesUtilisees= []

    def AllocPage(self) -> PageId :
        if (len(self.pagesDisponibles)!=0):
            self.pagesutilisees.append(self.pagesDisponibles[-1])
            return self.pagesDisponibles.pop()
        else:
            print("Aucune page disponible")
            return None

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