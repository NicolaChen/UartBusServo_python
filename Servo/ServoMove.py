from uart_servo.MyCheckSum import MyCheckSum as CheckSum
from pwm_servo.PCA9685 import PCA9685


class ServoMove:

    def __init__(self, my_serial, servo_id):
        self.serial = my_serial
        self.id = servo_id
        self.step_range = -1
        self.angle_range = 0
        self.servo_type = ""
        self.pwm = PCA9685(0x40)
        self.pwm.setPWMFreq(50)

        self.getStepRange()
        self.getAngleRange()
        self.getServoType()

    def getStepRange(self):

        step_range = [4096, 0, 0, 1024, 1000, 1024]
        self.step_range = step_range[self.id - 1]

    def getAngleRange(self):

        angle_range = [360, 360, 360, 300, 240, 300]
        self.angle_range = angle_range[self.id - 1]

    def getServoType(self):

        if self.step_range == 0:
            self.servo_type = "PWM"
        elif self.angle_range == 300:
            self.servo_type = "FTC"
        elif self.step_range == 1000:
            self.servo_type = "HW"
        elif self.step_range == 4096:
            self.servo_type = "FTT"
        else:
            print("Error, servo identification fail.")
            self.servo_type = "ERROR"

    def servoMove(self, angle, duration=0, speed=0):  # TODO: Figure out how duration and speed affect FTT/FTC/HW

        if angle > self.angle_range:
            angle = self.angle_range
        if self.servo_type == "PWM":
            pulse = 2000 * angle / self.angle_range + 500
            self.pwm.setServoPulse(self.id - 2, pulse)
        else:
            step = round(self.step_range * angle / self.angle_range)
            if self.servo_type == "FTT":
                self.serial.write(bytes(self.ftMoveT(step, duration, speed)))
            elif self.servo_type == "FTC":
                self.serial.write(bytes(self.ftMoveC(step, duration, speed)))
            elif self.servo_type == "HW":
                self.serial.write(bytes(self.hwMove(step, duration)))
            else:
                print("Servo move fail!")

    @staticmethod
    def getLowByte(val):
        return int(bin(val & 0xFF)[2:], 2)

    @staticmethod
    def getHighByte(val):
        return int(bin(val >> 8)[2:], 2)

    def ftMoveT(self, p, t, v):
        buf = [0 for _ in range(13)]
        buf[0] = buf[1] = 0xFF
        buf[2] = self.id
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

    def ftMoveC(self, p, t, v):
        buf = [0 for _ in range(13)]
        buf[0] = buf[1] = 0xFF
        buf[2] = self.id
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
        print('\n')

        return buf

    def hwMove(self, p, t):
        buf = [0 for _ in range(10)]
        buf[0] = buf[1] = 0x55
        buf[2] = self.id
        buf[3] = 7
        buf[4] = 1
        buf[5] = self.getLowByte(p)
        buf[6] = self.getHighByte(p)
        buf[7] = self.getLowByte(t)
        buf[8] = self.getHighByte(t)
        buf[9] = int(CheckSum(buf[2:-1]).get()[2:], 16)
        return buf
