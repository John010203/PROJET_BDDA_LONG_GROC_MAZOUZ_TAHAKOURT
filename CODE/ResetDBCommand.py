import BufferManager
import DataBaseInfo
import DiskManager

class ResetDBCommand():
    def __init__(self,bdd):
        """
        Initialise une instance de la classe ResetDBCommand
        """
        self.bdd = bdd
        self.diskManager = bdd.disk_manager
        self.bufferManager = bdd.buffer_manager
        self.databaseInfo = bdd.data_base_info

    def Execute(self):
        """
        Réinitialise la BDD en réinitialisant le diskManager, le bufferManager et dataBaseInfo
        """
        # print("-------------RESETDB-----------")
        self.diskManager.reset()
        self.bufferManager.reset()
        self.databaseInfo.reset()
        
        
        '''
         supprimer tous les fichiers du dossier DB
        • « remettre tout à 0 » dans le BufferManager et la DatabaseInfo, ainsi que potentiellement
        dans le DiskManager.
        Pour cela, il faut vider les listes, remettre tous les compteurs et les flags à 0, etc.
        Vous pouvez faire ces « remises à 0 » dans des méthodes spécifiques, à créer sur chaque
        classe concernée.
        '''