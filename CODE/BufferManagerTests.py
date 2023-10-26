from DiskManager import DiskManager
from BufferManager import BufferManager
from ByteBuffer import ByteBuffer
import DBParams as DP
from BDD import BDD

dbb = BDD(DP.DBParams("../DB",4096, 4, 10))


# DiskManager tests
dm = dbb.disk_manager
bf1= dbb.buffer_manager

bf = ByteBuffer(4096)
bf3 = ByteBuffer(4096)
bf4 = ByteBuffer(4096)

bf2 = ByteBuffer(4096)

bf.put_int(12)
bf.put_int(14)
bf.put_float(3.43)

page_id = dm.AllocPage()
print("file id : "+str(page_id.FileIdx)+" page id : "+str(page_id.PageIdx))
page_id2 = dm.AllocPage()
print("file id : "+str(page_id2.FileIdx)+" page id : "+str(page_id2.PageIdx))

# page_id3 = dm.AllocPage()
# page_id4 = dm.AllocPage()
# page_id5 = dm.AllocPage()


dm.WritePage(page_id, bf)

dm.ReadPage(page_id, bf2)
bf2.set_position(0)
print(bf2.read_int())
print(bf2.read_int())
print(bf2.read_float())
print(bf1.GetPage(page_id).to_bytes())

print('second getpage')
bf3 = bf1.GetPage(page_id)
print('troisieme getpage')
bf4 = bf1.GetPage(page_id2)
for e in bf1.listFrame:

    print(e.page_id.PageIdx,end=' ')

# bf1.FlushAll()
# bf5 = bf1.GetPage(page_id3)
# bf2 = bf1.GetPage(page_id4)


