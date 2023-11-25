import DBParams as DBP
from BDD import BDD
from DatabaseManager import DatabaseManager

'''
initialisation de la BDD
'''
bdd = BDD(DBP.DBParams("../DB/",4096, 4, 2))
diskManager = bdd.disk_manager
bfManager = bdd.buffer_manager

#test = DatabaseManager(bdd)