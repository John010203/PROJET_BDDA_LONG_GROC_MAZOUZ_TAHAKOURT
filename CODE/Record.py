import TableInfo as TableInfo

class Record : 
    def __init__(self, tableInfo):
        #relation a laquelle appartient le record
        self.tabInfo : TableInfo = tableInfo
        #valeurs du record -> un tuple a n vlauers (nb de cols dans la relation)
        self.recvalues : list = []

    def initTaille(self, indice):
        if(self.tabInfo.list[indice].typeColonne[0] == "VARCHAR(T)"):
            return len(self.recvalues[indice])
        else :
            return self.tabInfo.list[indice].typeColonne[1]
        
    def writeToBuffer(self, buff, pos) -> int :
        nbColonnes = len(self.recvalues)
        buff.set_position(pos)

        buff.put_int(self.initTaille(0))
        taille = self.initTaille(0)
        for j in range(1,nbColonnes):
            taille += self.initTaille(j)
            buff.put_int(taille)

        for i in range(nbColonnes):
            match self.tableInfo.cols[i].typeColonne[0] :
                case "INT": buff.put_int(self.recvalues[i])
                case "FLOAT" : buff.put_float(self.recvalues[i])
                case "STRING(T)" : 
                    for c in self.recvalues[i] :
                        buff.put_char(c)
        
        return taille #nb d'octets ecrits
    
    def readFromBuffer(self, buff, pos):
        nbColonnes = len(self.recvalues)
        tailleRecord = buff.read_int(pos + 4*(nbColonnes-1))
        
        buff.set_position(pos+4*nbColonnes)
        for i in range(nbColonnes):
            match self.tableInfo.cols[i].typeColonne[0] :
                case "INT": self.recvalues[i] = buff.read_int()
                case "FLOAT" : self.recvalues[i] = buff.read_float()
                case "STRING(T)" :  self.recvalues[i] = buff.read_char() #faut trouver la longueur de la chaine de caracteres
        return len(buff) - pos + 1
        