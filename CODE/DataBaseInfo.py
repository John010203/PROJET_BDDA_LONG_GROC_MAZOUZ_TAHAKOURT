import TableInfo as TableInfo

class DataBaseInfo :
    def __init__(self, db):
        self.db=db
        self.tableInfo : list = [] #toute sles relations de notre BDD
        #pas besoin de compteur size
        #pas besoin d'initialiser un compteur, on retourne jujste la taille du tableau
    def Init() -> None :
        #recuperer les definitions des tables, ecritent dans un fichier
        return
    
    def Finish() -> None:
        #ecrire les definitons des tables dans le fichier 
        return
    
    def getNbRelations(self) -> int:
        return len(self.tableInfo)
    
    def AddTableInfo(self, TableInfo : TableInfo) -> None:
        self.tableInfo.append(TableInfo)
    
    def GetTableInfo(self, nomRelation) -> TableInfo:
        for i in self.tableInfo : 
            if i.nomRelation == nomRelation :
                table = i
        return table