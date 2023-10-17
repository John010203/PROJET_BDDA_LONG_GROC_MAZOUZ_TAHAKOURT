import TableInfo as TableInfo
class DataBaseInfo :
    def init(self,tableInfo, compteur):
        self.tableInfo : list = tableInfo
        self.compteur : int = compteur

    def Init() -> None :
        return
    
    def Finish() -> None:
        return
    
    def AddTableInfo(self, TableInfo : TableInfo) :
        return self.tableInfo.append(TableInfo)
    
    def GetTableInfo(self, nomRelation) -> TableInfo:
        table : TableInfo = TableInfo()
        for i in self.tableInfo : 
            if i.nomRelation == nomRelation :
                table = i
        return table