class DeleteCommand:
    def __init__(self,chaineCommande,bdd):
        self.bdd=bdd
        self.commande = chaineCommande
        self.nomRelation,self.operations = self.parseCommandeDelete(chaineCommande)
    #DELETE FROM nomRelation WHERE nomColonne1OPvaleur1 nomColonne2OPvaleur2 AND nomColonnekOPvaleurk 
    def parseCommandeDelete(string):
        nomRelation = string.split(" ")[2].strip()
        if "WHERE" in string:
            condition = string.split("WHERE")[1].strip()
            listOp=[]
            # operations[-1] = operations.pop(-1)#why??
            if "AND" in condition:
                operations = condition.split("AND")
                for i in range(len(operations)):
                    operations[i]=operations[i].strip()#est ce qu'il faudrait metre un split()comme dans le select?
                return nomRelation,operations
            else:
                listOp.append(condition)
                return nomRelation,listOp
        else:
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
        colonneIndex = colonnes.index(opParsed[0])
        
        op1,op2 = opParsed[0],opParsed[1]
        tuples = self.bdd.file_manager.GetAllRecords(relation)

        match(operande):
            case ">=":
                return [i for i in tuples if self.cast(i[colonneIndex],relation,colonneIndex) >= self.cast(op2,relation,colonneIndex)]
            case "=<":
                return [i for i in tuples if self.cast(i[colonneIndex],relation,colonneIndex) <= self.cast(op2,relation,colonneIndex)]
            case ">":
                return [i for i in tuples if self.cast(i[colonneIndex],relation,colonneIndex) > self.cast(op2,relation,colonneIndex)]
            case "<":
                return [i for i in tuples if self.cast(i[colonneIndex],relation,colonneIndex) < self.cast(op2,relation,colonneIndex)]
            case "=":
                return [i for i in tuples if self.cast(i[colonneIndex],relation,colonneIndex) == self.cast(op2,relation,colonneIndex)]
            

    def Execute(self):
        print("-------------SUPPRESSION-----------")
        res = []
        if "WHERE" in self.commande :
            for op in self.operations:
                res+=self.evaluerOp(op)
        else : 
            relation = self.bdd.data_base_info.GetTableInfo(self.nomRelation)
            res = self.bdd.file_manager.GetAllRecords(relation)

        # for i in range(len(res)):
            #la il faut recuperer les recordId de la selection et les supprimer
            
        print("Tuples supprimes :",res)
        return 
