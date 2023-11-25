from TableInfo import TableInfo
from ColInfo import ColInfo 

class CreateTableCommand:

    def __init__(self,chaineCommande):
        self.commande = chaineCommande
        self.nomRelation,self.nbColonne,self.colInfos = self.parseCommandeCreateTable(chaineCommande)
    
    def parseCommandeCreateTable(self,string):
        print("DANS L AUTRE CLASSE")
        args = string[12:len(string)-1]
        nomRelation = (args.split('(')[0]).strip()
        cols = args.split('(')[1].split(',')
        listCols = []

        for c in cols:
            nomCol = c.split(':')[0]
            typeCol = c.split(':')[1]
            listCols.append(ColInfo(nomCol.strip(),typeCol.strip()))
        print(nomRelation,len(listCols),cols)
        return nomRelation,len(listCols),listCols
    
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
        