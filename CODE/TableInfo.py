from PageId import PageId

class TableInfo :
    def __init__(self,nomRelation,nbColonnes,cols,headerPageId : PageId):
        self.nomRelation = nomRelation
        self.nbColonne : int = nbColonnes
        self.cols : list = cols
        #self.headerPageId = headerPageId #PageId
    