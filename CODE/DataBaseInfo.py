import TableInfo as TableInfo
class DataBaseInfo :
    def __init__(self, db):
        self.db=db
        self.tableInfo : list = []
        #pas besoin de compteur size

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