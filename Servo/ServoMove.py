import time

import numpy as np
import serial

from Servo.pwm_servo.PCA9685 import PCA9685
from Servo.uart_servo.MyCheckSum import MyCheckSum as CheckSum


class ServoMove:

    def __init__(self):
        self.step_range = [4096, 0, 0, 1024, 1024, 1024]
        self.angle_range = [360, 360, 360, 300, 300, 300]
        self.servo_type = ["FTT", "PWM", "PWM", "FTC", "FTC", "FTC"]
        self.pwm_angle = [180, 180]

        self.serial = serial.Serial('/dev/ttyS4', 115200)
        self.pwm = PCA9685(0x40)
        self.pwm.setPWMFreq(50)
        self.pwm.setServoPulse(0, 1500)
        self.pwm.setServoPulse(1, 1500)

    def servoMove(self, angle_matrix):  # TODO: Figure out how duration and speed affect FTT/FTC

        serial_write_buf = []
        for i in range(6):
            angle = angle_matrix[i][0]
            if angle > self.angle_range[i]:
                angle = self.angle_range[i]

            if self.servo_type[i] != "PWM":
                step = round(self.step_range[i] * angle / self.angle_range[i])
                if self.servo_type[i] == "FTT":
                    buf_t = bytes(self.ftMoveT(i + 1, step, angle_matrix[i][1], angle_matrix[i][2]))
                    for j in buf_t:
                        serial_write_buf.append(j)
                elif self.servo_type[i] == "FTC":
                    buf_c = bytes(self.ftMoveC(i + 1, step, angle_matrix[i][1], angle_matrix[i][2]))
                    for k in buf_c:
                        serial_write_buf.append(k)
                else:
                    print("Servo%2d move fail!" % (i + 1))

        self.serial.write(serial_write_buf)
        print(serial_write_buf)

        old_angle_2 = self.pwm_angle[0]
        old_angle_3 = self.pwm_angle[1]
        angle_2 = angle_matrix[1][0]
        angle_3 = angle_matrix[2][0]
        time_gap = 0.05

        # solve 1
        # step = 20
        # for a, b in zip(np.linspace(old_angle_2, angle_2, step), np.linspace(old_angle_3, angle_3, step)):
        #     pulse_2 = 2000 * a / self.angle_range[1] + 500
        #     pulse_3 = 2000 * b / self.angle_range[2] + 500
        #     self.pwm.setServoPulse(0, pulse_2)
        #     self.pwm.setServoPulse(1, pulse_3)
        #     time.sleep(time_gap)

        # solve 2
        delta_x = 0.1
        for p in np.arange(np.pi / -2, np.pi / 2, delta_x):
            pulse_2 = 2000 * (old_angle_2 + (angle_2 - old_angle_2) * (np.sin(p) + 1) / 2)
            pulse_3 = 2000 * (old_angle_3 + (angle_3 - old_angle_3) * (np.sin(p) + 1) / 2)
            self.pwm.setServoPulse(0, pulse_2)
            self.pwm.setServoPulse(1, pulse_3)
            time.sleep(time_gap)

        self.pwm_angle[0] = angle_2
        self.pwm_angle[1] = angle_3

    @staticmethod
    def getLowByte(val):
        return int(bin(val & 0xFF)[2:], 2)

    @staticmethod
    def getHighByte(val):
        return int(bin(val >> 8)[2:], 2)

    def ftMoveT(self, n, p, t, v):
        buf = [0 for _ in range(13)]
        buf[0] = buf[1] = 0xFF
        buf[2] = n
        buf[3] = 9
        buf[4] = 3
        buf[5] = 0x2A
        buf[6] = self.getLowByte(p)
        buf[7] = self.getHighByte(p)
        buf[8] = self.getLowByte(t)
        buf[9] = self.getHighByte(t)
        buf[10] = self.getLowByte(v)
        buf[11] = self.getHighByte(v)
        print(CheckSum(buf[2:-1]).get()[2:])
        buf[12] = int(CheckSum(buf[2:-1]).get()[2:], 16)
        return buf

    def ftMoveC(self, n, p, t, v):
        buf = [0 for _ in range(13)]
        buf[0] = buf[1] = 0xFF
        buf[2] = n
        buf[3] = 9
        buf[4] = 3
        buf[5] = 0x2A
        buf[6] = self.getHighByte(p)
        buf[7] = self.getLowByte(p)
        buf[8] = self.getHighByte(t)
        buf[9] = self.getLowByte(t)
        buf[10] = self.getHighByte(v)
        buf[11] = self.getLowByte(v)
        buf[12] = int(CheckSum(buf[2:-1]).get()[2:], 16)
        print(buf)
        print(CheckSum(buf[2:-1]).get()[2:])
        return buf

    def closeSerial(self):
        self.serial.close()
        print("Serial has been closed!")
