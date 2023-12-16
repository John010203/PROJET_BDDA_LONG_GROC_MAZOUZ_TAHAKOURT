from ByteBuffer import ByteBuffer
import DBParams as DBP
from BDD import BDD
from Record import Record
from TableInfo import TableInfo
from ColInfo import ColInfo
from HeaderPage import HeaderPage
from DataPage import DataPage
from PageId import PageId
from RecordId import RecordId
'''
initialisation de la BDD
'''
bdd = BDD(DBP.DBParams("../DB/",4096, 4, 5))
diskManager = bdd.disk_manager
bfManager = bdd.buffer_manager
data_base_info = bdd.data_base_info
file_manager = bdd.file_manager

'''
CREATION D'UN HEADERPAGE
'''
headerPage = file_manager.createNewHeaderPage()
#premiere page de notre relation


"""
Creation tableInfo(relation)
"""
table = TableInfo("Personne",2,[ColInfo("Id",("INT",4)),ColInfo("Nom",("STRING(T)",5))],headerPage)
#tabVar = TableInfo("Prsn",2,[ColInfo("PRENOM",("VARCHAR(T)",15)),ColInfo("ID",("INT",4))],headerPage)
#print("Dans la table ->",table.headerPageId)

'''
CREATION Des RECORDS
'''
rec1 = Record(table,[1,"SIMBA"])
rec2 = Record(table,[2,"SMAIL"])
rec3 = Record(table,[3,"CHOPP"])


'''
ON AJOUTE UN PAGEID VIDE DANS LA LISTE CHAINEE

pageId = file_manager.addDataPage(table) #pageId vide
print(pageId)
'''
"""
ECRIRE LE RECORD DANS LE BUFFER
"""
#print('---------pageId1--------')
print('----------insert------------')
file_manager.InsertRecordIntoTable(rec1)
file_manager.InsertRecordIntoTable(rec2)
file_manager.InsertRecordIntoTable(rec3)

#print(file_manager.GetAllRecords(table))
pageId2 = PageId(1,0)
print('----------------read--------------')
print('stpppppppppppp',file_manager.getRecordsInDataPage(table,pageId2))
print('stpppppppppppp',file_manager.getRecordsInDataPage(table,pageId2)[0])
print('svpppppppppppp',file_manager.getRecordsInDataPage(table,pageId2)[1])
print('svpppppppppppp',file_manager.getRecordsInDataPage(table,pageId2)[2])

file_manager.DeleteRecordFromDataPage(RecordId(PageId(1,0),1))
print('----------------Apres suppression--------------')
print('stpppppppppppp',file_manager.getRecordsInDataPage(table,pageId2))
print('stpppppppppppp',file_manager.getRecordsInDataPage(table,pageId2)[0])
print('svpppppppppppp',file_manager.getRecordsInDataPage(table,pageId2)[1])
print('svpppppppppppp',file_manager.getRecordsInDataPage(table,pageId2)[2])

# print('svpppppppppppp',file_manager.getRecordsInDataPage(table,pageId2)[1])


#print('\n---------pageId2--------\n')
#pageId2 = file_manager.addDataPage(table)
#print(pageId2)
#file_manager.writeRecordToDataPage(rec3,pageId2)
#file_manager.getRecordsInDataPage(table,pageId2)[0]


#pageId2 = file_manager.addDataPage(table)
#print(pageId2)
#print('\n---------getFreePageId--------\n')
#HeaderPage(bfManager.GetPage(table.headerPageId))
#pageIdFree=file_manager.getFreeDataPageId(table,4049)

#print(bfManager)
#print(pageIdFree)

