from TableInfo import TableInfo
class CreateTableCommand:
    def __init__(self,nomRelation,nbColonnes,colInfos):
        self.nomRelation=nomRelation
        self.nbColonnes=nbColonnes
        self.colInfos=colInfos
    
    def Execute(self)->None:
        TableInfo(self.nomRelation,self.nbColonnes,self.colInfos)
        return