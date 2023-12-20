from RecordIterator import RecordIterator
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

    def evaluerJointure(self,tuple1,tuple2):
        #operation colonne>2
        #on split pour recup la colonne et la valeur
        relation1 = tuple1.tabInfo.nomRelation
        relation2 = tuple2.tabInfo.nomRelation
        colonnes1 = [i.nomColonne for i in tuple1.tabInfo.cols]
        colonnes2 = [i.nomColonne for i in tuple2.tabInfo.cols]
        bool=True

        for op in self.operations:#op = R1.C1 > R2.C2
            typeOperation=self.parseOperation(op) #operande= ">"
            opParsed=op.split(typeOperation)
            # print("opParsed : ", opParsed)
            relCol1=opParsed[0].split(".")#"[R1,C1]"
            relCol2=opParsed[1].split(".")#"[R2,C2]"
            colonne1 = colonnes1.index(relCol1[1].strip())#ca recupere la colonne dans la table
            # print("relCol1 : ", relCol1)
            # print("relCol2 : ", relCol2)
            colonne2 = colonnes2.index(relCol2[1].strip())
            # print("colonne 1 : ", colonne1)
            # print("colonne 2 : ", colonne2)
            
            match(typeOperation):
                case ">=":
                    bool = bool and tuple1.recvalues[colonne1] >= tuple2.recvalues[colonne2]
                case "<=":
                    bool = bool and tuple1.recvalues[colonne1] <= tuple2.recvalues[colonne2]
                case ">":
                    bool = bool and tuple1.recvalues[colonne1] > tuple2.recvalues[colonne2]
                case "<":
                    bool = bool and tuple1.recvalues[colonne1] < tuple2.recvalues[colonne2]
                case "=":
                    # print('egalite: ',tuple1.recvalues[colonne1])
                    # print('egalite: ',tuple2.recvalues[colonne2])
                    bool = bool and tuple1.recvalues[colonne1] == tuple2.recvalues[colonne2]
                case "<>":
                    bool = bool and tuple1.recvalues[colonne1] != tuple2.recvalues[colonne2]
                case "!=":
                    bool = bool and tuple1.recvalues[colonne1] != tuple2.recvalues[colonne2]
        return bool

    def parseOperation(self,op):#> < = >= <= <> !=
        """
        Extrait l'opérateur de comparaison
        """
        operationsSolo= ['>','<','=']
        operationsDuo = [">=","<=","<>","!="]
        
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
                case "<>":
                    bool = bool and tuple.recvalues[colonne] != self.cast(op2,relation,colonne)
                case "!=":
                    bool = bool and tuple.recvalues[colonne] != self.cast(op2,relation,colonne)
                    
        return bool 

    def executeSelectClassique(self):
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
        
        for t in unique:
            print(t)
        print('Total records=',len(unique))
  

    def executeJointure(self):
        r=self.bdd.data_base_info.GetTableInfo(self.nomRelation[0].strip())
        s=self.bdd.data_base_info.GetTableInfo(self.nomRelation[1].strip())
        rPages = self.bdd.file_manager.getDataPages(r)
        sPages = self.bdd.file_manager.getDataPages(s)
        # itr = RecordIterator(self.bdd, r,rPages[0])
        # its = RecordIterator(self.bdd, s,sPages[0])
        i,j=0,0
        nbTuples = 0
        if "WHERE" in self.commande :
            for rp in (rPages) : 
                itr = RecordIterator(self.bdd,r,rp)#GETPAGE
                nbSlotsR = itr.dataPage.getNbSlots(self.bdd)
                itr.Reset()
                for i in range(nbSlotsR) :
                    rt=itr.GetNextRecord(i)
                    for sp in sPages :
                        its = RecordIterator(self.bdd,s,sp)
                        nbSlotsS = its.dataPage.getNbSlots(self.bdd)
                        its.Reset()
                        for j in range(nbSlotsS):
                            st=its.GetNextRecord(j)
                            if self.evaluerJointure(rt,st):
                                nbTuples +=2
                                print(rt,'\n',st)
                        its.Close()
                        
                itr.Close()    
        else:
           for rp in (rPages) : 
                itr = RecordIterator(self.bdd,r,rp)#GETPAGE
                nbSlotsR = itr.dataPage.getNbSlots(self.bdd)
                itr.Reset()
                for i in range(nbSlotsR) :
                    rt=itr.GetNextRecord(i)
                    #print("rt : ",rt)
                    for sp in sPages :
                        its = RecordIterator(self.bdd,s,sp)
                        nbSlotsS = its.dataPage.getNbSlots(self.bdd)
                        its.Reset()
                        for j in range(nbSlotsS):
                            nbTuples +=2
                            print(rt,'\n',st)
                        its.Close()
                itr.Close()#freepage1    
        print('Total records : ',nbTuples)

    def Execute(self):
        """
        Exécute la commande SELECT et affiche les résultats
        """
        
        if type(self.nomRelation)==str :
            self.executeSelectClassique()   

        else:
            self.executeJointure()
        