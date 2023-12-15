from CreateTableCommand import CreateTableCommand
from ResetDBCommand import ResetDBCommand
from InsertCommand import InsertCommand
from SelectCommand import SelectCommand
from ImportCommand import ImportCommand
import pickle
import os
class DatabaseManager:

    def __init__(self,bdd):
        self.bdd=bdd
        self.diskManager = bdd.disk_manager
        self.bufferManager = bdd.buffer_manager
        self.databaseInfo = bdd.data_base_info

    def savedData(self):
        file = self.bdd.DBParams.DBPath+'DBInfo.save'
        data = []
        with open (file,'rb') as f1:
           if(os.path.getsize(file)>0):
                data =  pickle.load(f1)
        for relation in data :
            if relation != None:
                self.databaseInfo.AddTableInfo(relation)
                
        print('on recup les donnees saved',self.databaseInfo)
        
    def Finish(self):
        self.databaseInfo.Finish()
        self.bufferManager.FlushAll()
        self.diskManager.reset()

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
        if cmd == "RESETDB":
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
            ResetDBCommand(self.bdd).Execute()

        if self.insert(cmd):
            InsertCommand(cmd,self.bdd).Execute()

        if self.select(cmd):
            SelectCommand(cmd,self.bdd).Execute()

        if self.imprt(cmd):
            ImportCommand(cmd,self.bdd).Execute()
            