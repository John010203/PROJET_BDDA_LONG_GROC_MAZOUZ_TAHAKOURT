import TableInfo as TableInfo
import pickle
class DataBaseInfo :
    def __init__(self, db):
        self.db=db
        self.tableInfo : list = []
        #pas besoin de compteur size
        #pas besoin d'initialiser un compteur, on retourne jujste la taille du tableau

    #init lit un fichier et recupere  les definitions des tables    
    def Init(self) -> None :
        with open ('DBInfo','rb') as f1:
            self.tableInfo+= pickle.load(f1)
        
    #enregistre les definitions des tables
    def Finish(self) -> None:
        with open ('DBInfo','rb') as f1:
            pickle.dump(self.tableInfo,f1)
    
    def getNbRelations(self) -> int:
        return len(self.tableInfo)
    
    def AddTableInfo(self, TableInfo : TableInfo) -> None:
        self.tableInfo.append(TableInfo)
    
    def GetTableInfo(self, nomRelation) -> TableInfo:
        for i in self.tableInfo : 
            if i.nomRelation == nomRelation :
                table = i
        return table