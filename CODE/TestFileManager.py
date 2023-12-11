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
#premiere page de notre relation
#print("Header Page -> ",headerPage)

"""
Creation tableInfo(relation)
"""
table = TableInfo("Personne",2,[ColInfo("Id",("INT",4)),ColInfo("Nom",("STRING(T)",20))],headerPage)
#tabVar = TableInfo("Prsn",2,[ColInfo("PRENOM",("VARCHAR(T)",15)),ColInfo("ID",("INT",4))],headerPage)
#print("Dans la table ->",table.headerPageId)

'''
CREATION Des RECORDS
'''

rec = Record(table,[0,"SMAIL"])
rec2 = Record(table,[1,"SIMBA"])
rec3 = Record(table,[3,"CHOPPER"])


'''
ON AJOUTE UN PAGEID VIDE DANS LA LISTE CHAINEE
'''
pageId = file_manager.addDataPage(table) #pageId vide
print(pageId)

"""
ECRIRE LE RECORD DANS LE BUFFER
"""
#print('---------pageId1--------')
file_manager.writeRecordToDataPage(rec,pageId)
file_manager.writeRecordToDataPage(rec2,pageId)
file_manager.getRecordsInDataPage(table,pageId)[0]
file_manager.getRecordsInDataPage(table,pageId)[1]


print('\n---------pageId2--------\n')
pageId2 = file_manager.addDataPage(table)
print(pageId2)
file_manager.writeRecordToDataPage(rec3,pageId2)
file_manager.getRecordsInDataPage(table,pageId2)[0]

print('\n---------getFreePageId--------\n')
#HeaderPage(bfManager.GetPage(table.headerPageId))
pageIdFree=file_manager.getFreeDataPageId(table,4049)
#print(pageIdFree)

