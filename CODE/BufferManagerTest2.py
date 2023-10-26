from ByteBuffer import ByteBuffer
import DBParams as DBP
from BDD import BDD

'''
initialisation de la BDD
'''
bdd = BDD(DBP.DBParams("../DB/",4096, 4, 2))
diskManager = bdd.disk_manager
bfManager = bdd.buffer_manager



'''
Ecrire dans une page
'''
bfEcriture = ByteBuffer(4096)
#i can be your boyfriend hushhhhh
#ecrire dans le buffer
bfEcriture.put_char('L')
bfEcriture.put_int(0)
bfEcriture.put_char('L')
#Allocation de la page
pageId1 = diskManager.AllocPage()
diskManager.WritePage(pageId1,bfEcriture)
print('-----pageId1----',pageId1.FileIdx,pageId1.PageIdx,'----------')


'''
Lecture dans une page
'''
bfLecture = ByteBuffer(4096)#i can be your boyfriend hushhhhh
diskManager.ReadPage(pageId1,bfLecture)
print(bfLecture.read_char(),end=' ')
print(bfLecture.read_int(),end=' ')
print(bfLecture.read_char(),end=' ')

pageId2 = diskManager.AllocPage()
print('\n-----pageId2 ----',pageId2.FileIdx,pageId2.PageIdx)
diskManager.Dealloc(pageId1)
pageId3 = diskManager.AllocPage()
print('\n-----pageId2 ----',pageId3.FileIdx,pageId3.PageIdx)