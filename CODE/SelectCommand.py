
class SelectCommand:
    def __init__(self,chaineCommande,bdd):
        self.bdd =bdd
        self.commande = chaineCommande
        self.nomRelation,self.operations = self.parserCommandeSelect(chaineCommande)

    def parserCommandeSelect(self,string):
        nomRelation = string.split("FROM")[1].strip()
        if "," in nomRelation:
            return self.parserJointure(string)
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
    
    def parserJointure(self,string):
        relations=string.split("FROM")[1].split("WHERE ")[0].split(",")
        liste = []
        if "WHERE" in string:
            condition=string.split("WHERE ")[1]

            if "AND" in string:
                operations = condition.split("AND ")
                for c in operations : 
                    c = c.split()
            else :
                liste.append(condition)
                return relations,liste

            return relations,operations
        else : 
            return relations,[]


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

    def evaluerJointure(self,op):
        #operation colonne>2
        #on split pour recup la colonne et la valeur
        relation1 = self.bdd.data_base_info.GetTableInfo(self.nomRelation[0])
        relation2 = self.bdd.data_base_info.GetTableInfo(self.nomRelation[1])
        colonnes1 = [i.nomColonne for i in relation1]
        colonnes2 = [i.nomColonne for i in relation2]


        for op in self.operations:#op = R1.C1 > R2.C2
            typeOperation=self.parseOperation(op) #operande= ">"
            opParsed=op.split(typeOperation) 
            relCol1=self.parserOPJointure(opParsed[0])#"[R1,C1]"
            relCol2=self.parserOPJointure(opParsed[1])#"[R2,C2]"
            colonne1= colonnes1.index(relCol1[1])#ca recupere la colonne dans la table
            colonne2=colonnes2.index(relCol2[1])
            bool=True
            match(typeOperation):
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

            

        
        bool = True

    def parserOPJointure(self,opi):
        relCol=opi.split(".")
        relation=relCol[0]
        colonne=relCol[1]
        return relation,colonne
        

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

        