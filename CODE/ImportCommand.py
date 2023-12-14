from InsertCommand import InsertCommand
from Record import Record
class ImportCommand:
    #IMPORT INTO nomRelation nomFichier.csv
    def __init__(self,chaineCommande,bdd):
        self.bdd = bdd
        self.commande = chaineCommande
        self.nomRelation,self.nomFichier = self.parseCommandeImport(chaineCommande)
        
    def parseCommandeImport(self,string):
        return string.split(" ")[2].strip(),string.split(" ")[3].strip()
    
    def Execute(self)->None:
        print('-----------import----------------------')
        print('import'+self.bdd.data_base_info.__str__())
        
        insertion = InsertCommand("",self.bdd)
        insertion.nomRelation = self.nomRelation
        with  open("../"+self.nomFichier,"r") as fichier : 
            for ligne in fichier : 
                
                ligne = ligne.strip()
                relation = self.bdd.data_base_info.GetTableInfo(self.nomRelation)

                rec = Record(relation,ligne.split(","))
                insertion.values = rec

                insertion.Execute()
