import TableInfo as TableInfo

class Record : 
    def __init__(self, tableInfo,recvalues):
        #relation a laquelle appartient le record
        self.tabInfo : TableInfo = tableInfo
        #valeurs du record -> un tuple a n vlauers (nb de cols dans la relation)
        self.recvalues : list = recvalues

    def initTaille(self, indice):
        if(self.tabInfo.cols[indice].typeColonne[0] == "VARCHAR(T)"):
            return len(self.recvalues[indice])
        else :
            return self.tabInfo.cols[indice].typeColonne[1]
        
    def writeToBuffer(self, buff, pos) -> int :
        nbColonnes = len(self.recvalues)
        buff.set_position(pos)
        buff.put_int(self.initTaille(0))
        taille = self.initTaille(0)
        for j in range(1,nbColonnes):
            taille += self.initTaille(j)
            buff.put_int(taille)

        for i in range(nbColonnes):
            match self.tabInfo.cols[i].typeColonne[0] :
                case "INT": buff.put_int(self.recvalues[i])
                case "FLOAT" : buff.put_float(self.recvalues[i])
<<<<<<< HEAD
                case "STRING(T)" | "VARCHAR(T)": 
=======
                case "STRING(T)" :
                    
                    if len(self.recvalues[i])>0:
                        print('--',len(self.recvalues[i]))
                        for c in self.recvalues[i] :
                            buff.put_char(c)
                    for k in range(self.tabInfo.cols[i].typeColonne[1] - len(self.recvalues[i])):
                        buff.put_char(' ')
                        
                case "VARCHAR(T)": 
>>>>>>> DatabaseInfo
                    if(len(self.recvalues[i])>0):
                        for c in self.recvalues[i] :
                            buff.put_char(c)
                    else:
                        buff.put_char("N")
                        buff.put_char("O")
                        buff.put_char("N")
                        buff.put_char("E")
        
        return taille #nb d'octets ecrits
    
    def readFromBuffer(self, buff, pos):
        tabTaille : list = []
        nbColonnes = len(self.tabInfo.cols)
        buff.set_position(pos)
        for i in range(nbColonnes):
            tabTaille.append(buff.read_int()) 
        tailleRecord = tabTaille[-1]
        # buff.set_position(pos+4*nbColonnes) inutile??
        for i in range(nbColonnes):
<<<<<<< HEAD
            match self.tableInfo.cols[i].typeColonne[0] :
                case "INT": self.recvalues[i].append(buff.read_int())
                case "FLOAT" : self.recvalues[i].append(buff.read_float())
                case "STRING(T)" | "VARCHAR(T)" : 
                    self.recvalues[i].append("") #faut trouver la longueur de la chaine de caracteres
                    for j in range(tabTaille[i]-tabTaille[i-1] if i != 0 else tabTaille[i]):
                        self.recvalues[j]+=buff.read_char()
=======
            match self.tabInfo.cols[i].typeColonne[0] :
                case "INT": 
                    self.recvalues.append(buff.read_int())
                    
                case "FLOAT" : 
                    self.recvalues.append(buff.read_float())
                    
                case "STRING(T)" | "VARCHAR(T)" : 
                    self.recvalues.append(buff.read_char()) #faut trouver la longueur de la chaine de caracteres
                    for j in range(tabTaille[i]-tabTaille[i-1]-1 if i != 0 else tabTaille[i]-1):
                        self.recvalues[i]+=buff.read_char()
                    self.recvalues[i]=self.recvalues[i].strip()   
>>>>>>> DatabaseInfo
                case _:
                    print("erreur")    
        return tailleRecord
    
    def getTailleRecord(self):
        somme=0
        for i in range (len(self.recValues)):
            somme+=self.initTaille(i)
        return
        