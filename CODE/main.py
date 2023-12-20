
from DiskManager import DiskManager
import BufferManager as BM
from ByteBuffer import ByteBuffer
from TableInfo import TableInfo
from DataBaseInfo import DataBaseInfo
import DBParams as DP
from BDD import BDD
from DatabaseManager import DatabaseManager
from PageId import PageId


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

#CREATE TABLE PremiereRelation(Nom:STRING(20),Prenom:STRING(10))
#INSERT INTO PremiereRelation VALUES (Mazouz,Camelia)
#SELECT * FROM PremiereTable
#SELECT * FROM PremiereRelation WHERE Id=2 AND Id=0
def main():
    dataBaseManager = DatabaseManager(BDD(DP.DBParams("../DB/",4096, 4, 20)))
    run = True
    commande = ""
    dataBaseManager.savedData()
    while(run):
        commande = input("=>")
        if(commande == "EXIT"):
            dataBaseManager.Finish()
            run = False
        else:
            dataBaseManager.ProcessCommand(commande)
    buff = dataBaseManager.bdd.buffer_manager.GetPage(PageId(0,0))
    print(buff.read_int())
    print(buff.read_int())
    print(buff.read_int())
    print(buff.read_int())
    # with  open("commande.txt","r") as fichier : 
    #     for ligne in fichier : 
    #         ligne = ligne.strip()
    #         dataBaseManager.ProcessCommand(ligne)
    
    return
main()