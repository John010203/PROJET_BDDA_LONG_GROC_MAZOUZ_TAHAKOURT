
class SelectCommand:
    def __init__(self,chaineCommande,bdd):
        """
        Initialise une instance de la classe SelectCommand
        """
        self.bdd =bdd
        self.commande = chaineCommande
        self.nomRelation,self.operations = self.parserCommandeSelect(chaineCommande)

    def parserCommandeSelect(self,string):
        """
        Sépare la chaîne de commande pour extraire le nom de la relation et les opérations
        """
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
        """
        Extrait l'opérateur de comparaison
        """
        operationsSolo= ['>','<','=']
        operationsDuo = [">=","<="]
        
        for c in operationsDuo:
            if c in op:
                return c
        
        for c in operationsSolo:
            if c in op:
                return c
            
    def cast(self,valeur,relation,index):
        """
        Effectue une conversion de type pour la valeur en fonction du type de colonne
        """
        listType = [c.typeColonne[0] for c in relation.cols]

        if listType[index] == "INT":
            valeur = int(valeur)
        if listType[index] == "FLOAT":
            valeur = float(valeur)

        return valeur

    def evaluer(self,tuple):
        """
        Evalue toutes les opérations de sélection pour un tuple donné
        """
        #operation colonne>2
        #on split pour récup la colonne et la valeur
        relation = self.bdd.data_base_info.GetTableInfo(self.nomRelation)
        colonnes = [i.nomColonne for i in relation.cols]
        bool = True
        #test pour une seule colonne
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
                case "<=":
                    bool = bool and tuple.recvalues[colonne] <= self.cast(op2,relation,colonne)
                case ">":
                    bool = bool and tuple.recvalues[colonne] > self.cast(op2,relation,colonne)
                case "<":
                    bool = bool and tuple.recvalues[colonne] < self.cast(op2,relation,colonne)
                case "=":
                    bool = bool and tuple.recvalues[colonne] == self.cast(op2,relation,colonne)
                    
        return bool 
            

    def Execute(self):
        """
        Exécute la commande SELECT et affiche les résultats
        """
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

        