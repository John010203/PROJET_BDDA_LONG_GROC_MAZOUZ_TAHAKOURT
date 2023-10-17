from DiskManager import DiskManager
import BufferManager
from ByteBuffer import ByteBuffer
import DBParams as DP
from BDD import BDD

dbb = BDD(DP.DBParams("../DB",4096, 4, 2))


# DiskManager tests
dm = dbb.disk_manager
bf1= dbb.buffer_manager

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
bf1.GetPage(page_id).to_bytes()
bf1.GetPage(page_id).to_bytes()
bf1.GetPage(page_id).to_bytes()
bf1.GetPage(page_id).to_bytes()
bf1.GetPage(page_id).to_bytes()
bf1.GetPage(page_id).to_bytes()
print(bf1.GetPage(page_id).to_bytes())
print(bf1.GetPage(page_id).to_bytes())
print(bf1.GetPage(page_id).to_bytes())
print(bf1.GetPage(page_id).to_bytes())
print(bf1.GetPage(page_id).to_bytes())
print(bf1.GetPage(page_id).to_bytes())
print(bf1.GetPage(page_id).to_bytes())
print(bf1.GetPage(page_id).to_bytes())


