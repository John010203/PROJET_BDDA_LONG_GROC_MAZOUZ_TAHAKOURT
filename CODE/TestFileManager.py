from ByteBuffer import ByteBuffer
import DBParams as DBP
from BDD import BDD
from Record import Record
from TableInfo import TableInfo
'''
initialisation de la BDD
'''
bdd = BDD(DBP.DBParams("../DB/",4096, 4, 2))
diskManager = bdd.disk_manager
bfManager = bdd.buffer_manager
data_base_info = bdd.data_base_info
file_manager = bdd.file_manager

'''
CREATION D"UN RECORD
'''

rec = Record(bdd)

"""
Creation tableInfo(relation)
"""
table = TableInfo("Personne",2)
