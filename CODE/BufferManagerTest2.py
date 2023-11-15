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

#ecrire dans le buffer
bfEcriture.put_char('L')
print('------BUFFER ECRITURE------',bfEcriture)
bfEcriture.put_int(0)
bfEcriture.put_char('L')
bfEcriture.put_char('L')
#Allocation de la page
pageId1 = diskManager.AllocPage()
diskManager.WritePage(pageId1,bfEcriture)
#print('-----pageId1----',pageId1.FileIdx,pageId1.PageIdx,'----------')


'''
Lecture dans une page
'''
bfLecture = ByteBuffer(4096)
diskManager.ReadPage(pageId1,bfLecture)
print(bfLecture.read_char(),end=' ')
print(bfLecture.read_int(),end=' ')
print(bfLecture.read_char(),end=' ')
print(bfLecture.read_char(),end=' ')

pageId2 = diskManager.AllocPage()
#print('\n-----pageId2 ----',pageId2.FileIdx,pageId2.PageIdx)
diskManager.Dealloc(pageId1)
pageId3 = diskManager.AllocPage()
#print('\n-----pageId2 ----',pageId3.FileIdx,pageId3.PageIdx)

#print(bfManager.FindFrame(pageId1))
#print(bfManager.FindFrameLibre())


'''
Allocatioon de buffer depuis le buffer pool (bufferManager)
'''
Frame1 = bfManager.listFrame[bfManager.FindFrameLibre()]
Frame1.page_id = diskManager.AllocPage()
#print(Frame1.page_id)

Frame1.buffer.put_char('D')
Frame1.buffer.put_char('R')
Frame1.buffer.put_float(1.258)
Frame1.buffer.put_float(52251112)
Frame1.buffer.put_char('O')

diskManager.WritePage(Frame1.page_id,Frame1.buffer)
diskManager.ReadPage(Frame1.page_id,Frame1.buffer)

print(Frame1.buffer.read_char(),end=' ')
print(Frame1.buffer.read_char(),end=' ')
print(Frame1.buffer.read_float(),end=' ')
print(Frame1.buffer.read_float(),end=' ')
print(Frame1.buffer.read_char(),end=' ')

print(bfManager)

