from Servo.uart_servo.MyCheckSum import MyCheckSum as CheckSum
import time
import serial


def getLowByte(val):
    return int(bin(val & 0xFF)[2:], 2)


def getHighByte(val):
    return int(bin(val >> 8)[2:], 2)


def FTMove_T(servo_id, p, t, v):
    buf = [0 for _ in range(13)]
    buf[0] = buf[1] = 0xFF
    buf[2] = servo_id
    buf[3] = 9
    buf[4] = 3
    buf[5] = 0x2A
    buf[6] = getLowByte(p)
    buf[7] = getHighByte(p)
    buf[8] = getLowByte(t)
    buf[9] = getHighByte(t)
    buf[10] = getLowByte(v)
    buf[11] = getHighByte(v)
    print(CheckSum(buf[2:-1]).get()[2:])
    buf[12] = int(CheckSum(buf[2:-1]).get()[2:], 16)
    return buf


def FTMove_C(servo_id, p, t, v):
    buf = [0 for _ in range(13)]
    buf[0] = buf[1] = 0xFF
    buf[2] = servo_id
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
    print(buf)
    print(CheckSum(buf[2:-1]).get()[2:])
    print('\n')

    return buf


def HWMove(servo_id, p, t):
    buf = [0 for _ in range(10)]
    buf[0] = buf[1] = 0x55
    buf[2] = servo_id
    buf[3] = 7
    buf[4] = 1
    buf[5] = getLowByte(p)
    buf[6] = getHighByte(p)
    buf[7] = getLowByte(t)
    buf[8] = getHighByte(t)
    buf[9] = int(CheckSum(buf[2:-1]).get()[2:], 16)
    return buf


id_test = 4
pos = 980
stp = 2
k = 1
lim = 1023
mySerial = serial.Serial('/dev/ttyS4', 115200, 8)

# mySerial.write(bytes(ftMoveC(id, 0, 0, 0)))
while True:
    #    mySerial.write(bytes(ftMoveT(1, 300, 0, 0)))		#bytes() and bytearray() both work
    #    time.sleep(0.1)
    #    mySerial.write(bytes(hwMove(3, 481, 0)))
    #    time.sleep(0.1)
    #    mySerial.write(bytes(ftMoveC(4, 1023, 0, 0)))
    #    time.sleep(0.1)
    #    mySerial.write(bytes(ftMoveC(5, 0, 0, 0)))
    #    time.sleep(2)
    #    mySerial.write(bytes(ftMoveT(1, 800, 0, 0)))		#bytes() and bytearray() both work
    #    time.sleep(0.1)
    #    mySerial.write(bytes(hwMove(3, 451, 0)))
    #    time.sleep(0.1)
    #    mySerial.write(bytes(ftMoveC(4, 900, 0, 0)))
    #    time.sleep(0.1)
    #    mySerial.write(bytes(ftMoveC(5, 1023, 0, 0)))
    #    time.sleep(2)
    #    mySerial.write(bytes(ftMoveT(1, 2500-4, 0, 0)))		#bytes() and bytearray() both work
    #    time.sleep(0.1)
    #    mySerial.write(bytes(hwMove(3, 484, 0)))
    #    time.sleep(0.1)
    #    mySerial.write(bytes(ftMoveC(4,1003, 0, 0)))
    #    time.sleep(0.1)
    #    mySerial.write(bytes(ftMoveC(5, 512, 0, 0)))
    #    time.sleep(2)
    #    mySerial.write(bytes(ftMoveT(1, 2514+4, 0, 0)))		#bytes() and bytearray() both work
    #    time.sleep(0.1)
    #    mySerial.write(bytes(hwMove(3, 250, 0)))
    #    time.sleep(0.1)
    #    mySerial.write(bytes(ftMoveC(4, 900, 0, 0)))
    #    time.sleep(0.1)
    #    mySerial.write(bytes(ftMoveC(5, 256, 0, 0)))
    #    time.sleep(2)
    mySerial.write(bytes(FTMove_C(id_test, pos, 0, 0)))
    pos += k * stp
    if pos > lim:
        pos = lim
        k = -1
    elif pos <= 0:
        pos = 0
        k = 1
    time.sleep(1)
