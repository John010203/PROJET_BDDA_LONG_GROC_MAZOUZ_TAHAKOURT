from PageId import PageId

class TableInfo :
    def __init__(self,nomRelation,nbColonnes,cols,headerPageId : PageId):
        self.nomRelation = nomRelation
        self.nbColonne : int = nbColonnes
        self.cols : list = cols
        #self.headerPageId = headerPageId #PageId

    def __str__(self):
        return f"Table {self.nomRelation} with {len(self.cols)} columns"
    
    def save(self):
        res = self.nomRelation + "("
        for c in self.cols :
            res+= c.__str__()+","
        return res+")"