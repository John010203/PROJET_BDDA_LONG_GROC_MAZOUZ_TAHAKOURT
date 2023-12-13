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
        print('tg',pos)
        nbColonnes = len(self.recvalues)
        buff.set_position(0)
        buff.put_int(self.initTaille(0))
        taille = self.initTaille(0)
        print(nbColonnes)
        print('dans la boucle')
        for j in range(1,nbColonnes):
            print(buff.get_pos())
            taille += self.initTaille(j)
            buff.put_int(taille)
            print(buff.get_pos())
        print('hors la boucle')
        print('write to buffer taille pos ',taille,buff.get_pos())
        for i in range(nbColonnes):
            
            match self.tabInfo.cols[i].typeColonne[0] :
                case "INT": 
                    buff.put_int(self.recvalues[i])
                    buff.set_position(buff.get_pos()-4)
                    print(buff.read_int())
                case "FLOAT" : 
                    buff.put_float(self.recvalues[i])
                    buff.set_position(buff.get_pos()-4)
                    print(buff.read_float())
                case "STRING(T)" :
                    if len(self.recvalues[i])>0:
                        for c in self.recvalues[i] :
                            buff.put_char(c)
                            buff.set_position(buff.get_pos()-1)
                            print(buff.read_char())

                    for k in range(self.tabInfo.cols[i].typeColonne[1] - len(self.recvalues[i])):
                        buff.put_char(" ")
                        
                case "VARCHAR(T)": 
                    if(len(self.recvalues[i])>0):
                        for c in self.recvalues[i] :
                            buff.put_char(c)
                    else:
                        buff.put_char("N")
                        buff.put_char("O")
                        buff.put_char("N")
                        buff.put_char("E")
        buff.set_position(0)
        print('iciiiiiiiiiii',buff.read_int())
        print('iciiiiiiiiiii',buff.read_int())
        print('iciiiiiiiiiii',buff.read_int())
        print('iciiiiiiiiiii',buff.read_char())
        return taille #nb d'octets ecrits
    
    def readFromBuffer(self, buff, pos):
        #print('ICCIIIIIIIIIIIII',buff.read_char())
        tabTaille : list = []
        nbColonnes = len(self.tabInfo.cols)
        print('position',pos)
        buff.set_position(0)
        print('avant la boucle')
        for i in range(nbColonnes):
            tabTaille.append(buff.read_int()) 
        tailleRecord = tabTaille[-1]
        print('hors la boucle')
        # buff.set_position(pos+4*nbColonnes) inutile??
        print('readFromBuffer taille pos ',tailleRecord,buff.get_pos(),tabTaille)
        for i in range(nbColonnes):
            print('POS DU BUFFER',buff.get_pos())
            match self.tabInfo.cols[i].typeColonne[0] :
                case "INT": 
                    a = buff.read_int()
                    print(a)
                    self.recvalues.append(a)
                    
                case "FLOAT" : 
                    b = buff.read_float()
                    print(b)
                    self.recvalues.append(b)
                    
                case "STRING(T)" | "VARCHAR(T)" : 
                    self.recvalues.append(buff.read_char()) #faut trouver la longueur de la chaine de caracteres
                    for j in range(tabTaille[i]-tabTaille[i-1]-1 if i != 0 else tabTaille[i]-1):
                        self.recvalues[i]+=buff.read_char()
                    self.recvalues[i]=self.recvalues[i].strip()   
                    print('hahahahhahahaha',self.recvalues[i])
                case _:
                    print("erreur") 
        buff.set_position(0)   
        return tailleRecord
    
    def getTailleRecord(self):
        somme=0
        for i in range (len(self.recvalues)):
            somme+=self.initTaille(i)
        return somme
    
    def __str__(self):
        res = ""
        for i in self.recvalues :
            res += str(i)+ ' '
        return res
        