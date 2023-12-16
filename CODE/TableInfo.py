from PageId import PageId

class TableInfo :
    def __init__(self,nomRelation,nbColonnes,cols,headerPageId : PageId):
        self.nomRelation = nomRelation
        self.nbColonne : int = nbColonnes
        self.cols : list = cols
        self.headerPageId = headerPageId #PageId

    def __str__(self):
        res = f"Table {self.nomRelation} with"
        for c in self.cols :
            res += "\n\t- " + c.__str__()
        return res
    
    def save(self):
        res = str(self.nomRelation) + " " + str(self.nbColonne) + " " + str(self.headerPageId.FileIdx) + " " + str(self.headerPageId.PageIdx) + " "
        for c in self.cols :
            res+= c.__str__()+" " 
        return res
