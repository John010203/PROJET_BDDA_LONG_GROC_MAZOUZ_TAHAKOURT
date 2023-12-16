
class SelectCommand:
    def __init__(self,chaineCommande,bdd):
        self.bdd =bdd
        self.commande = chaineCommande
        self.nomRelation,self.operations = self.parserCommandeSelect(chaineCommande)

    def parserCommandeSelect(self,string):
        nomRelation = string.split("FROM")[1].strip()
        liste = []
        if "WHERE" in string:
            condition = string.split("WHERE")[1].strip()
            nomRelation = string.split("WHERE")[0][14:].strip()
            
            if "AND" in string:
                operations = condition.split("AND ")
                for c in operations : 
                    c = c.split()
                nbOperations = len(operations)
            else :
                liste.append(condition)
                return nomRelation,liste

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
                return [i for i in tuples if i.recvalues[colonne] >= self.cast(op2,relation,colonne)]
            case "=<":
                return [i for i in tuples if i.revalues[colonne] <= self.cast(op2,relation,colonne)]
            case ">":
                return [i for i in tuples if i.recvalues[colonne] > self.cast(op2,relation,colonne)]
            case "<":
                return [i for i in tuples if i.recvalues[colonne] < self.cast(op2,relation,colonne)]
            case "=":
                return [i for i in tuples if i.recvalues[colonne] == self.cast(op2,relation,colonne)]
        #pour toutes les colonnes op1 on check la valeur op2

        #un truc comme ca
        #apres on cherche parmis les tuples 
    #dans une operation ya 2 operandes et nomColonne> = < >= <=Valeur
    def evaluer(self,tuple):
        #operation colonne>2
        #on split pour recup la colonne et la valeur
        relation = self.bdd.data_base_info.GetTableInfo(self.nomRelation)
        colonnes = [i.nomColonne for i in relation.cols]
        bool = True
        #teste pour une seule colonne
        for op in self.operations:
            #on recupere l'operande
            operande = self.parseOperation(op)
            opParsed = op.split(operande)
            #on recupere la colonne
            colonne = colonnes.index(opParsed[0])
    
            op2 = opParsed[1]

            match(operande):
                case ">=":
                    bool = bool and tuple.recvalues[colonne] >= self.cast(op2,relation,colonne)
                case "=<":
                    bool = bool and tuple.revalues[colonne] <= self.cast(op2,relation,colonne)
                case ">":
                    bool = bool and tuple.recvalues[colonne] > self.cast(op2,relation,colonne)
                case "<":
                    bool = bool and tuple.recvalues[colonne] < self.cast(op2,relation,colonne)
                case "=":
                    bool = bool and tuple.recvalues[colonne] == self.cast(op2,relation,colonne)
                    
        return bool 
            

    def Execute(self):
        # print("-------------SELECTION-----------")
        unique = []
        relation = self.bdd.data_base_info.GetTableInfo(self.nomRelation)
        res = self.bdd.file_manager.GetAllRecords(relation)
        
        if "WHERE" in self.commande :
            for t in res:
                if self.evaluer(t):
                    unique.append(t)
        else :
            unique = res
        
        print(len(unique), 'tuples : ')
        for t in unique:
            print(t)

        