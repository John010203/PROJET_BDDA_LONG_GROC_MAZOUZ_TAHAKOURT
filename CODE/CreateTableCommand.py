from TableInfo import TableInfo
from ColInfo import ColInfo 

class CreateTableCommand:
    def __init__(self,nomRelation,nbColonnes,colInfos):
        self.nomRelation=nomRelation
        self.nbColonnes=nbColonnes
        self.colInfos=colInfos
    
    def Execute(self)->None:
        """
        appeler createNewHeaderPage du FileManager
        • créer une TableInfo en utilisant les données « communes », ainsi que le PageId rendu par
        l'appel à createHeaderPage ci-dessus
        • rajouter la TableInfo au DatabaseInfo avec la méthode qui convient
        """
        TableInfo(self.nomRelation,self.nbColonnes,self.colInfos)#faut rajouter le headerPage
        
        return
    

    #CREATE TABLE NomRelation (NomCol_1:TypeCol_1,NomCol_2:TypeCol_2,NomCol_NbCol:TypeCol_NbCol)
    def parseCommandeCreateTable(string):
        args = string[12:len(string)-1]
        nomRelation = args.split('(')[0]
        cols = args.split('(')[1].split(',')
        listCols = []

        for c in cols:
            nomCol = c.split(':')[0]
            typeCol = c.split(':')[1]
            listCols.append(ColInfo(nomCol,typeCol))

        return nomRelation,len(listCols),listCols
        