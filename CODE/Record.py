import TableInfo as TableInfo

class Record : 
    def __init__(self, tableinfo):
        self.tableinfo : TableInfo = tableinfo
        self.recvalues : list 

    def writeToBuffer(self, buff, pos) -> int :
        return
    def readFromBuffer(self, buff, pos):
        return