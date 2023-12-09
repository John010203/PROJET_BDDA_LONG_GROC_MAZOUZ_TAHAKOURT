import DataBaseInfo
from Record import Record
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
        chaineValeurs = args.split(',')
        relation = self.bdd.data_base_info.GetTableInfo(nomRelation)

        listType = [c.typeColonne[0] for c in relation.cols]
        
        for i in range(len(relation.cols)):
            if(listType[i] == "INT"):
                chaineValeurs[i] = int(chaineValeurs[i])
            if(listType[i] == "FLOAT"):
                chaineValeurs[i] = float(chaineValeurs[i])

        rec = Record(relation,chaineValeurs)
        #print(cols,end='\n')
        return nomRelation,rec
    
    def Execute(self):
        print("-------------INSERTION-----------")
        self.bdd.file_manager.InsertRecordIntoTable(self.values)
        return 0
