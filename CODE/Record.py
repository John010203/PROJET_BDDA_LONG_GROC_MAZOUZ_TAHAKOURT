import TableInfo as TableInfo

class Record : 
    def __init__(self, tableInfo):
        #relation a laquelle appartient le record
        self.tabInfo : TableInfo = tableInfo
        #valeurs du record -> un tuple a n vlauers (nb de cols dans la relation)
        self.recvalues : list = []

    def writeToBuffer(self, buff, pos) -> int :
        longueurDuRecord = len(self.recvalues)
        buff.set_position(pos)
        #taille fixe sans ecriture du offset directory
        #sinon on peut juste faire une boucle for et mettre les elements directement en bytes
        for i in range(longueurDuRecord):
            match self.tableInfo.cols[i].typeColonne :
                case "INT": buff.put_int(self.tableInfo.cols[i])
                case "FLOAT" : buff.put_float(self.tableInfo.cols[i])
                case "STRING(T)" : 
                    for c in self.tableInfo.cols[i] :
                        buff.put_char(c)
        return len(buff) - pos + 1
    
    def readFromBuffer(self, buff, pos):
        longueurDuRecord = len(self.recvalues)
        tailleColonne = None
        buff.set_position(pos)

        #taille fixe sans ecriture du offset directory
        #sinon on peut juste faire une boucle for et mettre les elements directement en bytes
        for i in range(longueurDuRecord):
            match self.tableInfo.cols[i].typeColonne :
                case "INT": buff.read_int()
                case "FLOAT" : buff.read_float()
                case "STRING(T)" :  buff.read_char() #faut trouver la longueur de la chaine de caracteres
        return len(buff) - pos + 1
        