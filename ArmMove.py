import time

from InverseKinematics import IK
from Servo.ServoMove import *


class ArmMove:

    def __init__(self):
        self.servos = ServoMove()
        self.p_j1_360 = 180
        self.p_j2_360 = 180
        self.p_j3_360 = 180
        self.p_j4_300 = 150
        self.p_j5_300 = 150
        self.p_j6_300 = 150
        self.servos.servoMove([[self.p_j1_360, 0, 0],
                               [self.p_j2_360, 0, 0],
                               [self.p_j3_360, 0, 0],
                               [self.p_j4_300, 0, 0],
                               [self.p_j5_300, 0, 0],
                               [self.p_j3_360, 0, 0]])
        self.angle_adjust = [180,
                             90,
                             90,
                             420,
                             240,
                             0]
        self.ik = IK()
        self.center = [150, 0, 100]
        print("Arm initialize complete.")

    def armCSInit(self):

        print("Begin coordinate system initialization.")
        while True:
            self.armMove(self.center)
            print("Arm has moved to center point.")
            time.sleep(4)
            while True:
                adjust_direction = input("Please input direction you want to adjust to, such as x/y/z.")
                if adjust_direction in ['x', 'y', 'z']:
                    break
                print("Invalid input! Try again.")
            while True:
                adjust_distance = input("Please input distance you want to adjust with, FLOAT is acceptable.")
                try:
                    if -500 < eval(adjust_distance) < 500:
                        break
                    print("Invalid input! Number too big.")
                except TypeError:
                    print("Invalid input! Not a number.")
            self.center[['x', 'y', 'z'].index(adjust_direction)] += adjust_distance
            print("New center: %s" % self.center)
            flag = input("Continue? y/n")
            if flag == 'n':
                break
            else:
                print("Continue arm center adjustment.")
        print("Arm center adjustment complete.")

    def servoMatGen(self, coordinate):

        res = self.ik.getJointsAngles(coordinate, 270, 180)
        return [[self.angle_adjust[0] + res['rot_j1'], 0, 0],
                [self.angle_adjust[1] + res['rot_j2'], 0, 0],
                [self.angle_adjust[2] + res['rot_j3'], 0, 0],
                [self.angle_adjust[3] - res['rot_j4'], 0, 0],
                [self.angle_adjust[4] - res['rot_j5'], 0, 0],
                [self.angle_adjust[5] + 0, 0, 0]]

    def armMove(self, coordinate):

        self.servos.servoMove(self.servoMatGen(coordinate))
