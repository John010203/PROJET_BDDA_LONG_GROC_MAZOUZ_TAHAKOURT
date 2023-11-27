
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
    
    def parseOperation(self,op):#> < = >= <=
        operationsSolo= ['>','<','=']
        operationsDuo = [">=","<="]
        
        for c in operationsDuo:
            if c in op:
                return c
        
        for c in operationsSolo:
            if c in op:
                return c
            
    def evaluerOp(self,op):
        op = op.strip()
        operande = self.parseOperation(op)
        op1,op2 = op.split(operande)
        #pour toutes les colonnes op1 on check la valeur op2
        #for c in cols :
        #   eval(c+operande+op2)
        #un truc comme ca
        #apres on cherche parmis les tuples 
    #dans une operation ya 2 operandes et nomColonne> = < >= <=Valeur
    def Execute(self):
        print("-------------SELECTION-----------")
        print()