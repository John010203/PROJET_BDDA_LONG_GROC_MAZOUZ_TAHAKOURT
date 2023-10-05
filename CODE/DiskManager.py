from PageId import PageId
from ByteBuffer import ByteBuffer

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
        numPage = pageId.PageIdx
        numFile = pageId.FileIdx
        pos = 4096*numPage
        file = open(self.bdd.DBParams.DBPath+"F"+str(numFile)+".data","rb")#revoir le seek
        buff.from_bytes(file.read(4096))
        file.close()
    
    def WritePage(self,pageId: PageId, buff) -> None:
        numPage = pageId.PageIdx
        numFile = pageId.FileIdx
        pos = 4096*numPage
        file = open(self.bdd.DBParams.DBPath+"F"+str(numFile)+".data","wb")
        file.write(buff.to_bytes())
        file.close()
        

    def Dealloc(self,pageId:PageId) -> None: 
        self.pagesDisponibles.append(pageId)

    def GetCurrentCountAllocPages(self) ->  int :
        """Retourne le nombre de pages allouées"""
        return sum(self.fileCounter)-len(self.pagesDisponibles)