from PageId import PageId
from ByteBuffer import ByteBuffer


class DiskManager :

    def __init__(self, bdd):
        self.bdd = bdd
        self.fileCounter = [0]*self.bdd.DBParams.DMFileCount
        self.pagesDisponibles = []

    def reset(self):
        self.fileCounter = [0]*self.bdd.DBParams.DMFileCount
        self.pagesDisponibles = []
        
    def AllocPage(self) -> PageId :
        if (len(self.pagesDisponibles)!=0):
            return self.pagesDisponibles.pop(0)
        else:
            index = self.fileCounter.index(min(self.fileCounter))
            self.fileCounter[index]+=1
            #VERIFIER QUE CA MARCHE DANSeq TOUS LES CAS
            return PageId(index, self.fileCounter[index]-1)

    def ReadPage(self,pageId: PageId, buff : ByteBuffer) -> None:
        numPage = pageId.PageIdx
        numFile = pageId.FileIdx
        pos = self.bdd.DBParams.SGBDPageSize*numPage
        file = open(self.bdd.DBParams.DBPath+"F"+str(numFile)+".data","rb")#revoir le seek
        file.seek(pos)
        buff.from_bytes(file.read(self.bdd.DBParams.SGBDPageSize))
        file.close()
    
    def WritePage(self,pageId: PageId, buff) -> None:
        numPage = pageId.PageIdx
        numFile = pageId.FileIdx
        pos = 4096*numPage
        with open(self.bdd.DBParams.DBPath+"F"+str(numFile)+".data","wb") as f:
            f.seek(pos)
            f.write(buff.to_bytes())

    def Dealloc(self,pageId:PageId) -> None: 
        self.pagesDisponibles.append(pageId)

    def GetCurrentCountAllocPages(self) ->  int :
        """Retourne le nombre de pages allouées"""
        return sum(self.fileCounter)-len(self.pagesDisponibles)
    
    def Init(self) -> None :
        with open (self.bdd.DBParams.DBPath+'DBDisk.save','r') as f1:
            # premier ligne info tablaux self.fileCounter et taille self.pagesDisponibles 
            param = f1.readline().split(" ")
            param[-1] = param[-1][:-1]
            for i in range(4):
                self.fileCounter[i] = int(param[i])
            nbPagesDisponibles = int(param[4])
            # les autre ligne represante les PageId
            for f in f1:
                self.pagesDisponibles.append(PageId(f.split(" ")[0], f.split(" ")[1]))
                
    def Finish(self) -> None:
        with open (self.bdd.DBParams.DBPath+'DBDisk.save','w') as f1:
            # premier ligne info tablaux self.fileCounter et taille self.pagesDisponibles 
            for i in range(4):
                f1.write(str(self.fileCounter[i]) + " ")
            f1.write(str(len(self.pagesDisponibles)) + "\n")
            for i in range(len(self.pagesDisponibles)):
                f1.write(str(self.pagesDisponibles[i].FileIdx) + " " + str(self.pagesDisponibles[i].PageIdx) + "\n")
            