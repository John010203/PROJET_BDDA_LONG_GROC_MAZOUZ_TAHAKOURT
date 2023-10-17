import TableInfo as TableInfo

class Record : 
    def init(self, tableinfo, recvalues):
        self.tableinfo : TableInfo = tableinfo
        self.recvalues : list = recvalues

    def writeToBuffer(self, buff, pos) -> int :
        return
    def readFromBuffer(self, buff, pos):
        return