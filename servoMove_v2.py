from myCheckSum import myCheckSum as CheckSum
import time
import serial


def getLowByte(val):
    return int(bin(val&0xFF)[2:], 2)

def getHighByte(val):
    return int(bin(val >> 8)[2:], 2)


def FTMove_T(id, p, t, v):
    buf = [0 for i in range(13)]
    buf[0] = buf[1] = 0xFF
    buf[2] = id
    buf[3] = 9
    buf[4] = 3
    buf[5] = 0x2A
    buf[6] = getLowByte(p)
    buf[7] = getHighByte(p)
    buf[8] = getLowByte(t)
    buf[9] = getHighByte(t)
    buf[10] = getLowByte(v)
    buf[11] = getHighByte(v)
    buf[12] = int(CheckSum(buf[2:-1]).get()[2:], 16)
    return buf

def FTMove_C(id, p, t, v):
    buf = [0 for i in range(13)]
    buf[0] = buf[1] = 0xFF
    buf[2] = id
    buf[3] = 9
    buf[4] = 3
    buf[5] = 0x2A
    buf[6] = getHighByte(p)
    buf[7] = getLowByte(p)
    buf[8] = getHighByte(t)
    buf[9] = getLowByte(t)
    buf[10] = getHighByte(v)
    buf[11] = getLowByte(v)
    buf[12] = int(CheckSum(buf[2:-1]).get()[2:], 16)
    return buf

def HWMove(id, p, t):
    buf = [0 for i in range(10)]
    buf[0] = buf[1] = 0x55
    buf[2] = id
    buf[3] = 7
    buf[4] = 1
    buf[5] = getLowByte(p)
    buf[6] = getHighByte(p)
    buf[7] = getLowByte(t)
    buf[8] = getHighByte(t)
    buf[9] = int(CheckSum(buf[2:-1]).get()[2:], 16)
    return buf

# def hexdump(src, line_size, prefix):
#     result = []
#     digits = 4 if isinstance(src, str) else 2

#     for i in range(0, len(src), line_size):
#         s = src[i:i + line_size]
#         hexa = ' '.join([hex(x)[2:].upper().zfill(digits) for x in s])
#         text = ''.join([chr(x) if 0x20 <= x < 0x7F else '.' for x in s])
#         result.append(prefix + ' | ' + hexa.ljust(line_size * (digits + 1)) + ' |' + "{0}".format(text) + '|')

#     return '\n'.join(result)

# print("spi mode: 0x%x" % args.mode)
# print("max speed: %d Hz (%d KHz)\n" %(args.speed, args.speed / 1000), end='')

# print(default_tx)
# print(FTMove(1, 2048, 0, 1000))

mySerial = serial.Serial('/dev/ttyS4', 115200, 8)
while True:
    mySerial.write(bytes(FTMove_T(1, 0, 0, 0)))		#bytes() and bytearray() both work
    time.sleep(0.1)
    mySerial.write(bytes(HWMove(3, 0, 0)))
    time.sleep(0.1)
    mySerial.write(bytes(FTMove_C(4, 0, 0, 0)))
    time.sleep(0.1)
    mySerial.write(bytes(FTMove_C(5, 0, 0, 0)))
    time.sleep(4)
    mySerial.write(bytes(FTMove_T(1, 4095, 0, 0)))		#bytes() and bytearray() both work
    time.sleep(0.1)
    mySerial.write(bytes(HWMove(3, 1000, 0)))
    time.sleep(0.1)
    mySerial.write(bytes(FTMove_C(4, 1023, 0, 0)))
    time.sleep(0.1)
    mySerial.write(bytes(FTMove_C(5, 1023, 0, 0)))
    time.sleep(4)
    mySerial.write(bytes(FTMove_T(1, 2048, 0, 0)))		#bytes() and bytearray() both work
    time.sleep(0.1)
    mySerial.write(bytes(HWMove(3, 500, 0)))
    time.sleep(0.1)
    mySerial.write(bytes(FTMove_C(4, 512, 0, 0)))
    time.sleep(0.1)
    mySerial.write(bytes(FTMove_C(5, 512, 0, 0)))
    time.sleep(4)
    mySerial.write(bytes(FTMove_T(1, 1024, 0, 0)))		#bytes() and bytearray() both work
    time.sleep(0.1)
    mySerial.write(bytes(HWMove(3, 250, 0)))
    time.sleep(0.1)
    mySerial.write(bytes(FTMove_C(4, 256, 0, 0)))
    time.sleep(0.1)
    mySerial.write(bytes(FTMove_C(5, 256, 0, 0)))
    time.sleep(4)

