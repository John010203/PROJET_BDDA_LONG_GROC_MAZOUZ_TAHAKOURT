class ImportCommand:
    #IMPORT INTO nomRelation nomFichier.csv
    def __init__(self,chaineCommande):
        self.commande = chaineCommande
        self.nomRelation,self.nomFichier = self.parseCommandeImport(chaineCommande)
        
    def parseCommandeImport(self,string):
        return string.split(" ")[2].strip(),string.split(" ")[3].strip()
    
    def Execute(self)->None:
        #contenu csv : 97,180,25,23,0 dnas chaque ligne ya un record
        #parser une ligne
        print("------------IMPORT COMMAND-------------")
        fichier = open("../"+self.nomFichier,"r")
        #on recupere les tuples
        tuples = fichier.readlines()
        #les valeurs sont separees par des virgules
        #diskManager et record et buffermanager
        #for t in tuples :
        #   on ecrit le tuple dans un buffer
        #   r = Record(self.nomRelation,t)
        #   r.writeToBuffer()
        #   on ecrit le tuple dans un fichier
        #   self.bdd.disk_manager.writePage(pageId,buff)

        return