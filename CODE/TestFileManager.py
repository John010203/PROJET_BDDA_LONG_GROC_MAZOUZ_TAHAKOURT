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
#headerPage = file_manager.createNewHeaderPage()

"""
Creation tableInfo(relation)
"""
#table = TableInfo("Personne",2,[ColInfo("Id",("INT",4)),ColInfo("Nom",("STRING(T)",20))],headerPage)
#tabVar = TableInfo("Prsn",2,[ColInfo("PRENOM",("VARCHAR(T)",15)),ColInfo("ID",("INT",4))],)



'''
CREATION D"UN RECORD
'''

#rec = Record(table,[0,"SMAIL"])
#rec2 = Record(table,[1,"SIMBA"])
#rec3 = Record(table,[3,"CHOPPER"])
#recVide = Record(table,[])

'''
ON AJOUTE UN PAGEID VIDE DANS LA LISTE CHAINEE
'''
#pageId = file_manager.addDataPage(table) #pageId vide


"""
ECRIRE LE RECORD DANS LE BUFFER
"""
#file_manager.writeRecordToDataPage(rec,pageId)

#file_manager.writeRecordToDataPage(rec3,pageId)

#print(file_manager.getRecordsInDataPage(table,pageId)[0])
#print(file_manager.getRecordsInDataPage(table,pageId)[1])
#print(file_manager.getRecordsInDataPage(table,pageId)[2])
#print('---------pageid2--------')
#pageId2 = file_manager.addDataPage(table)

#file_manager.writeRecordToDataPage(rec2,pageId2)
#bf = bfManager.GetPage(pageId2)
#bf.set_position(0)
#print(bf.read_int())
#print(bf.read_int())
#pageIdNeutre = PageId()
#pageId = diskManager.AllocPage()
#bf = bfManager.GetPage(pageId)
#dataPage = DataPage(bf)
#dataPage.setPageId(pageIdNeutre)


'''
test getpage
'''
#print('fngjkdherbgouryhgieufhipguepig')
pageId = diskManager.AllocPage()
pageId2 = diskManager.AllocPage()

print('----',bfManager.GetPage(pageId))
print('----',bfManager.GetPage(pageId2))

bfManager.FreePage(pageId,False)

pageId3 = diskManager.AllocPage()
print('----',bfManager.GetPage(pageId3))

bfManager.FreePage(pageId2,False)

pageId4 = diskManager.AllocPage()
print('----',bfManager.GetPage(pageId4))


bfManager.FreePage(pageId3,False)

pageId5 = diskManager.AllocPage()
print('----',bfManager.GetPage(pageId5))

bfManager.FreePage(pageId4,False)

pageId6 = diskManager.AllocPage()
print('----',bfManager.GetPage(pageId6))