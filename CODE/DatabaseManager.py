from CreateTableCommand import CreateTableCommand
from ResetDBCommand import ResetDBCommand
from InsertCommand import InsertCommand
from SelectCommand import SelectCommand
from ImportCommand import ImportCommand
class DatabaseManager:

    def __init__(self,bdd):
        self.bdd=bdd
        self.diskManager = bdd.disk_manager
        self.bufferManager = bdd.buffer_manager
        self.databaseInfo = bdd.data_base_info

    def Finish(self):
        self.databaseInfo.Finish()
        self.bufferManager.FlushAll()

    def createTable(self,cmd):
        typeComande = cmd.split(' ')
        if typeComande[0] == "CREATE" and typeComande[1] == "TABLE":
            return True
        else :
            return False
        
    def insert(self,cmd):
        typeComande = cmd.split(' ')
        if typeComande[0] == "INSERT":
            return True
        else :
            return False
        
    def select(self,cmd):
        typeComande = cmd.split(' ')
        if typeComande[0] == "SELECT":
            return True
        else :
            return False

    def reset(self,cmd):
        typeComande = cmd.split(' ')
        if typeComande[0] == "RESETDB":
            return True
        else :
            return False
    def imprt(self,cmd):
        typeComande = cmd.split(' ')
        if typeComande[0] == "IMPORT" and typeComande[1] == "INTO":
            return True
        else :
            return False

    def ProcessCommand(self, cmd : str):
        
        if self.createTable(cmd):
            CreateTableCommand(cmd,self.bdd).Execute()
        if self.reset(cmd):
            ResetDBCommand(cmd).Reset()
        if self.insert(cmd):
            InsertCommand(cmd,self.bdd).Execute()
        if self.select(cmd):
            SelectCommand(cmd).Execute()
        if self.imprt(cmd):
            ImportCommand(cmd,self.bdd).Execute()
            