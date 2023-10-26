import ByteBuffer as ByteBuffer
import sys
buffer = ByteBuffer.ByteBuffer()
buffer.put_int(13)
buffer.put_int(-24)
buffer.put_float(3.2)
buffer.put_char('T')
buffer.put_char('P')

buffer.set_position(0)
print(buffer.read_int())
print(buffer.read_int())
print(buffer.read_float())
print(buffer.read_char())
print(buffer.read_char())

with open("buffer.txt", 'wb') as f:
    f.seek(20)
    f.write(buffer.to_bytes())

    f.seek(10)
    f.write(buffer.to_bytes())

buffer = ByteBuffer.ByteBuffer(0)
with open("buffer.txt", 'rb') as f:
    buffer.from_bytes(f.read()[20:50])

    print(buffer.read_int())
    print(buffer.read_int())
    print(buffer.read_float())
    print(buffer.read_char())
    print(buffer.read_char())

with open("buffer.txt", 'rb') as f:
    buffer.from_bytes(f.read()[10:40])

    print(buffer.read_int())
    print(buffer.read_int())
    print(buffer.read_float())
    print(buffer.read_char())
    print(buffer.read_char())

'''
b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13
\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;
<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abc
'''