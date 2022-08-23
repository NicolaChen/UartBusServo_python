#!/usr/bin/env python3
# encoding:utf-8
import time

import numpy as np

from InverseKinematics import *

# 机械臂根据逆运动学算出的角度进行移动
ik = IK()
# 设置连杆长度

ik.setLinkLength()


class ArmIK:
    """USELESS"""
    def __init__(self):
        pass

    def transformAngelAdaptArm(self, theta3, theta4, theta5, theta6):
        # 将逆运动学算出的角度转换为舵机对应的脉宽值
        servo3 = int(round(theta3 * self.servo3Param + (self.servo3Range[1] + self.servo3Range[0]) / 2))
        if servo3 > self.servo3Range[1] or servo3 < self.servo3Range[0] + 60:
            logger.info('servo3(%s)超出范围(%s, %s)', servo3, self.servo3Range[0] + 60, self.servo3Range[1])
            return False

        servo4 = int(round(theta4 * self.servo4Param + (self.servo4Range[1] + self.servo4Range[0]) / 2))
        if servo4 > self.servo4Range[1] or servo4 < self.servo4Range[0]:
            logger.info('servo4(%s)超出范围(%s, %s)', servo4, self.servo4Range[0], self.servo4Range[1])
            return False

        servo5 = int(round((self.servo5Range[1] + self.servo5Range[0]) / 2 - (90.0 - theta5) * self.servo5Param))
        if servo5 > ((self.servo5Range[1] + self.servo5Range[0]) / 2 + 90 * self.servo5Param) or servo5 < (
                (self.servo5Range[1] + self.servo5Range[0]) / 2 - 90 * self.servo5Param):
            logger.info('servo5(%s)超出范围(%s, %s)', servo5, self.servo5Range[0], self.servo5Range[1])
            return False

        if theta6 < -(self.servo6Range[3] - self.servo6Range[2]) / 2:
            servo6 = int(
                round(((self.servo6Range[3] - self.servo6Range[2]) / 2 + (90 + (180 + theta6))) * self.servo6Param))
        else:
            servo6 = int(round(((self.servo6Range[3] - self.servo6Range[2]) / 2 - (90 - theta6)) * self.servo6Param))
        if servo6 > self.servo6Range[1] or servo6 < self.servo6Range[0]:
            logger.info('servo6(%s)超出范围(%s, %s)', servo6, self.servo6Range[0], self.servo6Range[1])
            return False

        return {"servo3": servo3, "servo4": servo4, "servo5": servo5, "servo6": servo6}

    def servosMove(self, servos, movetime=None):
        # 驱动3,4,5,6号舵机转动
        time.sleep(0.02)
        if movetime is None:
            max_d = 0
            for i in range(0, 4):
                d = abs(getBusServoPulse(i + 3) - servos[i])
                if d > max_d:
                    max_d = d
            movetime = int(max_d * 4)
        setBusServoPulse(3, servos[0], movetime)
        setBusServoPulse(4, servos[1], movetime)
        setBusServoPulse(5, servos[2], movetime)
        setBusServoPulse(6, servos[3], movetime)

        return movetime

    def setPitchRange(self, coordinate_s, rot_1, rot_2, delta, step):
        # 给定坐标coordinate_s和俯仰角的范围alpha1，alpha2, 自动在范围内寻找到的合适的解
        # 如果无解返回False,否则返回对应舵机角度,俯仰角
        # 坐标单位cm， 以元组形式传入，例如(0, 5, 10)
        # da为俯仰角遍历时每次增加的角度
        for a, b in zip(np.arange(rot_1, rot_1 + delta * step / abs(step), step),
                        np.arange(rot_2, rot_2 + delta * step / abs(step), step)):  # 遍历求解
            result = ik.getJointsAngles(coordinate_s, a, b)
            if result:
                theta3, theta4, theta5, theta6 = result['theta3'], result['theta4'], result['theta5'], result['theta6']
                servos = self.transformAngelAdaptArm(theta3, theta4, theta5, theta6)
                if servos != False:
                    return servos, alpha

        return False

    def setPitchRangeMoving(self, coordinate_s, rot_j4, rot_j5, r_rot_j4, r_rot_j5, move_time=None):
        # 给定坐标coordinate_s、滚转角rot_j4和俯仰角rot_j5，以及两角的范围r_rot_j4、r_rot_j5，自动寻找最接近给定两角的解，并转到目标位置
        # 如果无解返回False,否则返回舵机角度、滚转角、俯仰角、运行时间
        # 坐标单位mm， 以元组形式传入，例如(0, 50, 100)
        # move_time为舵机转动时间，单位ms, 如果不给出时间，则自动计算
        x, y, z = coordinate_s
        for a, b in zip(np.arange(rot_j4 - r_rot_j4, rot_j4 + r_rot_j4, 1),
                        np.arange(rot_j5 - r_rot_j5, rot_j5 + r_rot_j5, 1)):
            res = ik.getJointsAngles(coordinate_s, a, b)

        result1 = self.setPitchRange((x, y, z), rot_j4, r_rot_j4)
        result2 = self.setPitchRange((x, y, z), rot_j5, r_rot_j5)
        if result1 != False:
            data = result1
            if result2 != False:
                if abs(result2[1] - alpha) < abs(result1[1] - alpha):
                    data = result2
        else:
            if result2 != False:
                data = result2
            else:
                return False
        servos, alpha = data[0], data[1]

        move_time = self.servosMove((servos["servo3"], servos["servo4"], servos["servo5"], servos["servo6"]), move_time)

        return servos, alpha, move_time

    '''
    #for test
    def drawMoveRange2D(self, x_min, x_max, dx, y_min, y_max, dy, z, a_min, a_max, da):
        # 测试可到达点, 以2d图形式展现，z固定
        #测试可到达点, 以3d图形式展现，如果点过多，3d图会比较难旋转
        try:
            for y in np.arange(y_min, y_max, dy):
                for x in np.arange(x_min, x_max, dx):
                    result = self.setPitchRange((x, y, z), a_min, a_max, da)
                    if result:
                        plt.scatter(x, y, s=np.pi, c='r')

            plt.xlabel('X Label')
            plt.ylabel('Y Label')

            plt.show()
        except Exception as e:
            print(e)
            pass

    def drawMoveRange3D(self, x_min, x_max, dx, y_min, y_max, dy, z_min, z_max, dz, a_min, a_max, da):
        #测试可到达点, 以3d图形式展现，如果点过多，3d图会比较难旋转
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        try:
            for z in np.arange(z_min, z_max, dz):
                for y in np.arange(y_min, y_max, dy):
                    for x in np.arange(x_min, x_max, dx):
                        result = self.setPitchRange((x, y, z), a_min, a_max, da)
                        if result:
                            ax.scatter(x, y, z, s=np.pi, c='r')

            ax.set_xlabel('X Label')
            ax.set_ylabel('Y Label')
            ax.set_zlabel('Z Label')

            plt.show()
        except Exception as e:
            print(e)
            pass
    '''


if __name__ == "__main__":
    AK = ArmIK()
    setBusServoPulse(1, 200, 500)
    setBusServoPulse(2, 500, 500)
    # AK.setPitchRangeMoving((0, 10, 10), -30, -90, 0, 2000)
    # time.sleep(2)
    print(AK.setPitchRangeMoving((-4.8, 15, 1.5), 0, -90, 0, 2000))
    # AK.drawMoveRange2D(-10, 10, 0.2, 10, 30, 0.2, 2.5, -90, 90, 1)
