import DataBaseInfo
from Record import Record
class InsertCommand : 

    def __init__(self,chaineCommande,bdd):
        self.bdd = bdd
        self.commande = chaineCommande
        self.nomRelation,self.values = self.parserCommandeInsert(chaineCommande)

    #INSERT INTO nomRelation VALUES (val1,val2,valn)

    def parserCommandeInsert(self,string):
        if string != "":
            values = string.split("VALUES")[1].strip()
            args = values[1:len(values)-1]
            nomRelation = (string.split(' ')[2]).strip()
            chaineValeurs = args.split(',')
            relation = self.bdd.data_base_info.GetTableInfo(nomRelation)

            listType = [c.typeColonne[0] for c in relation.cols]
            
            for i in range(len(relation.cols)):
                if(listType[i] == "INT"):
                    chaineValeurs[i] = int(chaineValeurs[i])
                if(listType[i] == "FLOAT"):
                    chaineValeurs[i] = float(chaineValeurs[i])

            rec = Record(relation,chaineValeurs)
            return nomRelation,rec
        return "",""
    
    def Execute(self):
        self.bdd.file_manager.InsertRecordIntoTable(self.values)
        return 0
