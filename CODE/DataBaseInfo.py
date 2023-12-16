from TableInfo import TableInfo
from PageId import *
from ColInfo import *
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
        with open (self.db.DBParams.DBPath+'DBInfo.save','r') as f1:
            for f in f1:
                param = f.split(" ")
                nomRelation = param[0]
                nbColonnes = int(param[1])
                headerPageId = PageId(int(param[2]), int(param[3]))
                cols = []
                print('++++++',param)
                for c in range(4, nbColonnes*2+3, 2):
                    print('dans la boucle',param[c].split(":")[0], (param[c].split(":")[1], int(param[c+1])))
                    cols.append(ColInfo(param[c].split(":")[0], (param[c].split(":")[1], int(param[c+1]))))
                self.tableInfo.append(TableInfo(nomRelation, nbColonnes, cols, headerPageId))

    #--------------------------------------------------------------------------------------------------------------
    #enregistre les definitions des tables
    def Finish(self) -> None:
        with open (self.db.DBParams.DBPath+'DBInfo.save','w') as f1:
            for tb in self.tableInfo:
                f1.write(tb.save())

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