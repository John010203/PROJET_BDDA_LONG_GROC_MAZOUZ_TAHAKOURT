from PageId import PageId
class DataPage : 
    def __init__(self,buff):
        #buff devra contenir les PageId et les donnees
        self.buff = buff


    def initialisation(self):
        self.buff.set_position(4088)#
        self.buff.put_int(0)#nb slots
        self.buff.put_int(8)#debut espace libre
        self.buff.set_position(0)

    def setPageId(self,pageId):
        self.buff.set_position(0)
        self.buff.put_int(pageId.FileIdx)
        self.buff.put_int(pageId.PageIdx)
        self.buff.set_position(0)

    def nextPageId(self):
        self.buff.set_position(0)
        pageId = PageId(self.buff.read_int(),self.buff.read_int())
        self.buff.set_position(0)
        return pageId

    def getPosition(): return
    def setPosition(pos):return
    def getRecordAt(pos):return 
    def getEspaceDisponible(self):
        self.buff.set_position(4096-8)
        nbSlot = self.buff.read_int()
        posFreeArea = self.buff.read_int()
        self.buff.set_position(0)
        return 4096-(nbSlot*8)-posFreeArea-8
    
    def getNbSlots(self,bdd):
        self.buff.set_position(bdd.DBParams.SGBDPageSize-8)
        nbSlots = self.buff.read_int()
        self.buff.set_position(0)
        return nbSlots
    
    def getdebutEspaceDispo(self,bdd):
        self.buff.set_position(bdd.DBParams.SGBDPageSize-4)
        espaceDispo = self.buff.read_int()
        self.buff.set_position(0)
        return espaceDispo
    
    def setNbSlots(self, nbSlots,bdd):
        self.buff.set_position(bdd.DBParams.SGBDPageSize-8)
        self.buff.put_int(nbSlots)
        self.buff.set_position(0)

    def setdebutEspaceDispo(self,espaceDispo ,bdd):
        self.buff.set_position(bdd.DBParams.SGBDPageSize-4)
        self.buff.put_int(espaceDispo)
        self.buff.set_position(0)

    def putNewSlot(self,bdd,tailleRecord):
        nbSlot = self.getNbSlots(bdd)
        debutEspaceDispo = self.getdebutEspaceDispo(bdd)
        self.buff.set_position(bdd.DBParams.SGBDPageSize-16-(nbSlot*8))
        self.buff.put_int(debutEspaceDispo)
        self.buff.put_int(tailleRecord)
        self.buff.set_position(0)
    