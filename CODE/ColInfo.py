class ColInfo : 
    def __init__(self, nomColonne, typecolonne):
        self.types = ["INT","FLOAT","STRING(T)","VARSTRING(T)"]
        self.nomColonne = nomColonne
        self.typeColonne = typecolonne #(TYPE DE LA COLONNE,TAILLE DU TYPE)

    def __str__(self):
        return ""+self.nomColonne+":"+self.typeColonne[0] +" "+str(self.typeColonne[1])