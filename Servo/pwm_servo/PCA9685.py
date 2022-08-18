import time
import math
import smbus


class PCA9685:
    # Registers/etc.
    __SUBADR1 = 0x02
    __SUBADR2 = 0x03
    __SUBADR3 = 0x04
    __MODE1 = 0x00
    __PRESCALE = 0xFE
    __LED0_ON_L = 0x06
    __LED0_ON_H = 0x07
    __LED0_OFF_L = 0x08
    __LED0_OFF_H = 0x09
    __ALLLED_ON_L = 0xFA
    __ALLLED_ON_H = 0xFB
    __ALLLED_OFF_L = 0xFC
    __ALLLED_OFF_H = 0xFD

    def __init__(self, address=0x40, debug=False):
        self.bus = smbus.SMBus(8)
        self.address = address
        self.debug = debug
        if self.debug:
            print("Resetting PCA9685")
        self.write(self.__MODE1, 0x00)

    def write(self, reg, value):
        """Writes an 8-bit value to the specified register/address"""
        self.bus.write_byte_data(self.address, reg, value)
        if self.debug:
            print("I2C: Write 0x%02X to register 0x%02X" % (value, reg))

    def read(self, reg):
        """Read an unsigned byte from the I2C device"""
        result = self.bus.read_byte_data(self.address, reg)
        if self.debug:
            print("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (self.address, result & 0xFF, reg))
        return result

    def setPWMFreq(self, freq):
        """Sets the PWM frequency"""
        pre_scale_val = 25000000.0  # 25MHz
        pre_scale_val /= 4096.0  # 12-bit
        pre_scale_val /= float(freq)
        pre_scale_val -= 1.0
        if self.debug:
            print("Setting PWM frequency to %d Hz" % freq)
            print("Estimated pre-scale: %d" % pre_scale_val)
        pre_scale = math.floor(pre_scale_val + 0.5)
        if self.debug:
            print("Final pre-scale: %d" % pre_scale)

        old_mode = self.read(self.__MODE1)
        new_mode = (old_mode & 0x7F) | 0x10  # sleep
        self.write(self.__MODE1, new_mode)  # go to sleep
        self.write(self.__PRESCALE, int(math.floor(pre_scale)))
        self.write(self.__MODE1, old_mode)
        time.sleep(0.005)
        self.write(self.__MODE1, old_mode | 0x80)

    def setPWM(self, channel, on, off):
        """Sets a single PWM channel"""
        self.write(self.__LED0_ON_L + 4 * channel, on & 0xFF)
        self.write(self.__LED0_ON_H + 4 * channel, on >> 8)
        self.write(self.__LED0_OFF_L + 4 * channel, off & 0xFF)
        self.write(self.__LED0_OFF_H + 4 * channel, off >> 8)
        if self.debug:
            print("channel: %d  LED_ON: %d LED_OFF: %d" % (channel, on, off))

    def setServoPulse(self, channel, pulse):
        """Sets the Servo Pulse,The PWM frequency must be 50HZ"""
        pulse = round(pulse * 4096 / 20000)  # PWM frequency is 50HZ,the period is 20000us
        self.setPWM(channel, 0, pulse)
