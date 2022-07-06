from myCheckSum import myCheckSum as CheckSum
import wiringpi
import argparse
import time

parser = argparse.ArgumentParser(description='')
parser.add_argument("--channel", type=int, default=1, help='specify the spi channel')
parser.add_argument("--port", type=int, default=0, help='specify the spi port')
parser.add_argument("--speed", type=int, default=115200, help='specify the spi speed')
parser.add_argument("--mode", type=int, default=0, help='specify the spi mode')
args = parser.parse_args()

# default_tx = [
#         0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
#         0x40, 0x00, 0x00, 0x00, 0x00, 0x95,
#         0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
#         0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
#         0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
#         0xF0, 0x0D,
# ]

def getLowByte(val):
    return int(bin(val&0xFF)[2:], 2)

def getHighByte(val):
    return int(bin(val >> 8)[2:], 2)

def FTMove(id, p, t, v):
    buf = [0 for i in range(13)]
    buf[0] = buf[1] = 0xFF
    buf[2] = id
    buf[3] = 0x09
    buf[4] = 0x03
    buf[5] = 0x2A
    buf[6] = getLowByte(p)
    buf[7] = getHighByte(p)
    buf[8] = getLowByte(t)
    buf[9] = getHighByte(t)
    buf[10] = getLowByte(v)
    buf[11] = getHighByte(v)
    buf[12] = int(CheckSum(buf).get()[2:], 16)
    
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
wiringpi.wiringPiSPISetupMode(args.channel, args.port, args.speed, args.mode)
for i in range(10):
    revlen, recvData = wiringpi.wiringPiSPIDataRW(args.channel, bytes(FTMove(0x03, 2048, 0, 0)))
    time.sleep(2)
    revlen, recvData = wiringpi.wiringPiSPIDataRW(args.channel, bytes(FTMove(0x03, 4095, 0, 0)))
    time.sleep(2)
    revlen, recvData = wiringpi.wiringPiSPIDataRW(args.channel, bytes(FTMove(0x03, 0, 0, 0)))
    time.sleep(2)
