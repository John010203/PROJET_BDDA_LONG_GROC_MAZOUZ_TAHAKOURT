import DataBaseInfo
import Record
class InsertCommand : 

    def __init__(self,chaineCommande,bdd):
        self.bdd = bdd
        self.commande = chaineCommande
        self.nomRelation,self.values = self.parserCommandeInsert(chaineCommande)

    #INSERT INTO nomRelation VALUES (val1,val2,valn)

    def parserCommandeInsert(self,string):
        values = string.split("VALUES")[1].strip()
        args = values[1:len(values)-1]
        #print(args,end='\n')
        nomRelation = (string.split(' ')[2]).strip()
        #print(nomRelation,end='\n')
        cols = args.split(',')
        #print(cols,end='\n')
        
        return nomRelation,cols
    
    def Execute(self):
        print("-------------INSERTION-----------")
        #on cherche la relation dans la BDD
        relation = self.bdd.data_base_info.GetTableInfo(self.nomRelation)
        #diskManager et record et buffermanager
        #avec diskManager et la fonction write to buffer de ricord on save les donnnes dans un fichier
        #apres faut ecrire ces donnes dans un fichier 
        return 0
