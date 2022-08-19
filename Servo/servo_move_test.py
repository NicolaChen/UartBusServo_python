import time

from ServoMove import ServoMove

s = ServoMove()

s.servoMove([[300, 0, 0],
             [180, 0, 0],
             [180, 0, 0],
             [120, 0, 0],
             [100, 0, 0],
             [180, 0, 0]])

time.sleep(2)

s.servoMove([[180, 0, 0],
             [120, 0, 0],
             [270, 0, 0],
             [30, 0, 0],
             [150, 0, 0],
             [0, 0, 0]])

s.closeSerial()
