from ByteBuffer import ByteBuffer
import DBParams as DBP
from BDD import BDD
from Record import Record
from TableInfo import TableInfo
from ColInfo import ColInfo
from HeaderPage import HeaderPage
from DataPage import DataPage
from PageId import PageId
'''
initialisation de la BDD
'''
bdd = BDD(DBP.DBParams("../DB/",4096, 4, 2))
diskManager = bdd.disk_manager
bfManager = bdd.buffer_manager
data_base_info = bdd.data_base_info
file_manager = bdd.file_manager

'''
CREATION D'UN HEADERPAGE
'''
headerPage = file_manager.createNewHeaderPage()


"""
Creation tableInfo(relation)
"""
table = TableInfo("Personne",2,[ColInfo("Id",("INT",4)),ColInfo("Nom",("STRING(T)",20))],headerPage)
tabVar = TableInfo("Prsn",2,[ColInfo("PRENOM",("VARCHAR(T)",15)),ColInfo("ID",("INT",4))],headerPage)



'''
CREATION D"UN RECORD
'''

rec = Record(table,[0,"SMAIL"])
rec2 = Record(table,[1,"SIMBA"])
rec3 = Record(table,[3,"CHOPPER"])


'''
ON AJOUTE UN PAGEID VIDE DANS LA LISTE CHAINEE
'''
pageId = file_manager.addDataPage(table) #pageId vide
bf=bfManager.GetPage(pageId)
bf.set_position(0)
print(pageId)
print(bf.read_int())
bfManager.FreePage(pageId,False)


"""
ECRIRE LE RECORD DANS LE BUFFER
"""

file_manager.writeRecordToDataPage(rec,pageId)
file_manager.writeRecordToDataPage(rec2,pageId)
file_manager.writeRecordToDataPage(rec3,pageId)

print(file_manager.getRecordsInDataPage(table,pageId)[0])
print(file_manager.getRecordsInDataPage(table,pageId)[1])

print('-----------------')
pageId2 = file_manager.addDataPage(table)
file_manager.writeRecordToDataPage(rec2,pageId2)
print(pageId2)

#HeaderPage(bfManager.GetPage(table.headerPageId))
pageIdFree=file_manager.getFreeDataPageId(table,4049)
print(pageIdFree)



