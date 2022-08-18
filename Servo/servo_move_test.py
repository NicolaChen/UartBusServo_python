from ServoMove import ServoMove
import serial
import time

mySerial = serial.Serial('/dev/ttyS4', 115200)
s1 = ServoMove(mySerial, 1)
s2 = ServoMove(mySerial, 2)
s3 = ServoMove(mySerial, 3)
s4 = ServoMove(mySerial, 4)
s5 = ServoMove(mySerial, 5)
s6 = ServoMove(mySerial, 6)

s2.servoMove(151)
s3.servoMove(255.43)
time.sleep(2)
s2.servoMove(340.2)
s3.servoMove(0)
