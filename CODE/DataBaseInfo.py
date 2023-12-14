import TableInfo as TableInfo
import pickle

class DataBaseInfo :
    def __init__(self, db):
        self.db=db
        self.tableInfo : list = [] #toute sles relations de notre BDD
        #pas besoin de compteur size
        #pas besoin d'initialiser un compteur, on retourne jujste la taille du tableau
    def reset(self):
        self.tableInfo = []
    #init lit un fichier et recupere  les definitions des tables    
    def Init(self) -> None :
        with open (self.db.DBParams.DBPath+'DBInfo.save','rb') as f1:
            self.tableInfo+= pickle.load(f1)
    #--------------------------------------------------------------------------------------------------------------
    #enregistre les definitions des tables
    def Finish(self) -> None:
        with open (self.db.DBParams.DBPath+'DBInfo.save','wb') as f1:
            pickle.dump(self.tableInfo,f1)
        
        with open (self.db.DBParams.DBPath+'DBInfo.save','rb') as f1:
           data =  pickle.load(f1)

        print(data.__str__())
    #--------------------------------------------------------------------------------------------------------------
    def getNbRelations(self) -> int:
        return len(self.tableInfo)
    
    def AddTableInfo(self, TableInfo : TableInfo) -> None:
        self.tableInfo.append(TableInfo)
    
    def GetTableInfo(self, nomRelation) -> TableInfo:
        table = None
        for i in self.tableInfo : 
            if i.nomRelation == nomRelation :
                table = i
        return table
    
    def __str__(self):
        res = ""
        for t in self.tableInfo:
            res+=("\n"+t.__str__())
        return res