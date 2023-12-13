
class SelectCommand:
    def __init__(self,chaineCommande,bdd):
        self.bdd =bdd
        self.commande = chaineCommande
        self.nomRelation,self.operations = self.parserCommandeSelect(chaineCommande)

    def parserCommandeSelect(self,string):
        nomRelation = nomRelation = string.split("FROM")[1].strip()
        if "WHERE" in string:
            condition = string.split("WHERE")[1].strip()
            #SELECT * FROM nomRelation WHERE 
            nomRelation = string.split("WHERE")[0][14:].strip()
            
            if "AND" in string:
                operations = condition.split("AND ")
                nbOperations = len(operations)
                print(nbOperations)
            else :
                return nomRelation,[].append(condition)
              
            return nomRelation,operations
        else : 
            return nomRelation,[]
    
    def parseOperation(self,op):#> < = >= <=
        operationsSolo= ['>','<','=']
        operationsDuo = [">=","<="]
        
        for c in operationsDuo:
            if c in op:
                return c
        
        for c in operationsSolo:
            if c in op:
                return c
    def cast(self,valeur,relation,index):
        listType = [c.typeColonne[0] for c in relation.cols]

        if listType[index] == "INT":
            valeur = int(valeur)
        if listType[index] == "FLOAT":
            valeur = float(valeur)

        return valeur

    def evaluerOp(self,op):

        opParsed = op.split(self.parseOperation(op))

        relation = self.bdd.data_base_info.GetTableInfo(self.nomRelation)
        colonnes = [i.nomColonne for i in relation.cols]

        operande = self.parseOperation(op)
        colonne = colonnes.index(opParsed[0])
        
        op1,op2 = opParsed[0],opParsed[1]
        tuples = self.bdd.file_manager.GetAllRecords(relation)

        match(operande):
            case ">=":
                return [i for i in tuples if i[colonne] >= self.cast(op2,relation,colonne)]
            case "=<":
                return [i for i in tuples if i[colonne] <= self.cast(op2,relation,colonne)]
            case ">":
                return [i for i in tuples if i[colonne] > self.cast(op2,relation,colonne)]
            case "<":
                return [i for i in tuples if i[colonne] < self.cast(op2,relation,colonne)]
            case "=":
                return [i for i in tuples if i[colonne] == self.cast(op2,relation,colonne)]
        #pour toutes les colonnes op1 on check la valeur op2

        #un truc comme ca
        #apres on cherche parmis les tuples 
    #dans une operation ya 2 operandes et nomColonne> = < >= <=Valeur
    def Execute(self):
        print("-------------SELECTION-----------")
        res = []
        if not(self.operations) :
            for op in self.operations:
                res.append(self.evaluerOp(op))
        else : 
            relation = self.bdd.data_base_info.GetTableInfo(self.nomRelation)
            res = self.bdd.file_manager.GetAllRecords(relation)
        print(res)