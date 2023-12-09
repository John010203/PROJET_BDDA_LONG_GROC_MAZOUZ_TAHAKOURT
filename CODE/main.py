
from DiskManager import DiskManager
import BufferManager as BM
from ByteBuffer import ByteBuffer
from TableInfo import TableInfo
from DataBaseInfo import DataBaseInfo
import DBParams as DP
from BDD import BDD
from DatabaseManager import DatabaseManager


'''
#dbb.DataBaseInfo.add 

# DiskManager tests
dm = dbb.disk_manager

bf = ByteBuffer(4096)
bf2 = ByteBuffer(4096)

bf.put_int(12)
bf.put_int(14)
bf.put_float(3.43)

page_id = dm.AllocPage()
dm.WritePage(page_id, bf)

dm.ReadPage(page_id, bf2)
print(bf2.read_int())
print(bf2.read_int())
print(bf2.read_float())

print(dm.GetCurrentCountAllocPages())
dm.Dealloc(page_id)
print(dm.GetCurrentCountAllocPages())
'''

#CREATE TABLE NomRelation (NomCol_1:TypeCol_1,NomCol_2)
#CREATE TABLE PremiereRelation(Nom:STRING(20),Prenom:STRING(10))
#INSERT INTO PremiereRelation VALUES (Mazouz,Camelia)

def main():
    dataBaseManager = DatabaseManager(BDD(DP.DBParams("../DB/",4096, 4, 2)))
    run = True
    commande = ""
    while(run):
        commande = input("=>")
        if(commande == "EXIT"):
            dataBaseManager.Finish()
            run = False
        else:
            dataBaseManager.ProcessCommand(commande)
    
    
    return
main()