
class SelectCommand:
    def __init__(self,chaineCommande):
        self.commande = chaineCommande
        self.nomRelation,self.operations = self.parserCommandeSelect(chaineCommande)

    def parserCommandeSelect(self,string):
        condition = string.split("WHERE")[1].strip()
        operations = condition.split("AND ")
        print(condition,end='\n')
        print(operations,end='\n')
        
        nomRelation = string.split("WHERE")[0][14:].strip()
        print(nomRelation,end='\n')
        
        nbOperations = len(operations)
        print(nbOperations)
        return nomRelation,operations
    
    def parseOperation(op):
        return 
    #dans une operation ya 2 operandes et nomColonne> = < >= <=Valeur
    def Execute(self):
        print("-------------SELECTION-----------")
        print()