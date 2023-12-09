from TableInfo import TableInfo
from ColInfo import ColInfo

class CreateTableCommand:

    def __init__(self,chaineCommande,db):
        self.db = db
        self.commande = chaineCommande
        self.nomRelation,self.nbColonne,self.colInfos = self.parseCommandeCreateTable(chaineCommande)
    
    def parseCommandeCreateTable(self,string):
        #print("DANS L AUTRE CLASSE")
        args = string[12:len(string)-1]
        nomRelation = (args.split('(')[0]).strip()
        cols = args.split(nomRelation+'(')[1].split(',')
        listCols = []

        for c in cols:
            nomCol = c.split(':')[0]
            typeCol = c.split(':')[1]
            if "STRING" in typeCol:
                typeCol = ("STRING", int(typeCol.split("(")[1][:-1]))
            if "VARCHAR" in typeCol:
                typeCol = ("VARCHAR", int(typeCol.split("(")[1][:-1]))
            if "INT" in typeCol:
                typeCol = ("INT", 4)
            if "FLOAT" in typeCol:
                typeCol = ("FLOAT", 4)

            listCols.append(ColInfo(nomCol.strip(),typeCol))
        #print(nomRelation,len(listCols),cols)
        return nomRelation,len(listCols),listCols
    
    def Execute(self)->None:
        headerPage = self.db.file_manager.createNewHeaderPage()
        relation = TableInfo(self.nomRelation,self.nbColonne,self.colInfos,headerPage)
        self.db.data_base_info.AddTableInfo(relation)

        print(self.db.data_base_info)
        
        return
    

    #CREATE TABLE NomRelation (NomCol_1:TypeCol_1,NomCol_2:TypeCol_2,NomCol_NbCol:TypeCol_NbCol)
        