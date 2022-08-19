import logging
from math import *

# CRITICAL, ERROR, WARNING, INFO, DEBUG
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class IK:
    # 舵机从下往上数
    # 公用参数，三维图纸测量获得，单位为mm和deg
    h1b = 0  # 一号舵机到水平底面到距离
    a210 = 0  # l12与水平面的夹角
    l12 = 0  # 底盘中心到二号舵机的距离
    l23 = 0  # 二号舵机到三号舵机的距离
    l35 = 0  # 三号舵机到五号舵机的连线距离
    a435 = 0  # 四号关节处定向线与l35连线到夹角
    l5s = 0  # 五号舵机到气动夹爪中心到距离

    def __init__(self):
        pass

    def setLinkLength(self, h_1b=h1b, a_210=a210, l_12=l12, l_23=l23, l_35=l35, l_5s=l5s, a_435=a435):

        self.h1b = h_1b
        self.a210 = a_210  # 钝角
        self.l12 = l_12
        self.l23 = l_23
        self.l35 = l_35
        self.l5s = l_5s
        self.a435 = a_435

    def getLinkLength(self):

        return {"h1b": self.h1b, "l12": self.l12, "a210": self.a210, "l23": self.l23, "l35": self.l35,
                "a435": self.a435, "l5s": self.a435}

    # 给定指定坐标和末端所需4、5关节转角，返回每个关节应该旋转的角度，如果无解返回False
    # coordinate为夹爪末端中心坐标，坐标单位mm， 以元组形式传入，例如(0, 5, 10)
    # beta4为夹爪所需关节4的转角，以初始态为例，视向平面即为YZ平面；
    # beta5为夹爪所需关节5的转角，以初始态为例，视向平面即为ZX平面；转角单位deg
    # 设夹持器末端为end(X, Y, Z), 坐标原点为origin(0, 0, 0), 原点为底盘转盘中心在台面的投影， end点在地面的投影为end_p
    # 初始零位定义：关节1为使臂主体正对工作区，关节4为使45转臂平行正对工作区域，关节5为使5s夹爪铅垂正对工作区域
    # 空间坐标轴放置标准：初始零位下，关节1与工作区中心连线为x轴，臂主体位于ZX平面，z轴垂直与工作平面向上；平面内逆时针旋转角度为正

    def getJointsAngles(self, coordinate_s, rot_j4, rot_j5):

        x, y, z = coordinate_s
        x0 = x + self.l5s * sin(rot_j5)
        y0 = y - self.l5s * cos(rot_j5) * sin(rot_j4)
        z0 = z + self.l5s * cos(rot_j5) * cos(rot_j4)

        rot_j1 = degrees(atan2(y0, x0))  # 求底座旋转角度
        dis_hor_5_2 = sqrt(x0 ** 2 + y0 ** 2) - self.l12 * cos(self.a210)  # end_p到关节2的水平距离
        dis_ver_5_2 = z0 - self.l12 * sin(self.a210)

        if self.l23 + self.l35 * sin(self.a435) < dis_hor_5_2:  # 两边之和小于第三边
            logger.debug('不能构成连杆结构, l23(%s) + l35sin(%s) < AC(%s)', self.l23, self.l35 * sin(self.a435),
                         dis_hor_5_2)
            return False

        cos_3p = (self.l23 ** 2 + self.l35 ** 2 - dis_ver_5_2 ** 2 - dis_hor_5_2 ** 2) / (2 * self.l23 * self.l35)
        cos_2p = (self.l23 ** 2 + dis_ver_5_2 ** 2 + dis_hor_5_2 ** 2 - self.l35 ** 2) / \
                 (2 * self.l23 * sqrt(dis_ver_5_2 ** 2 + dis_hor_5_2 ** 2))

        if abs(cos_3p) > 1:
            logger.debug('不能构成连杆结构, abs(cos_3p(%s)) > 1', cos_3p)
            return False
        rot_j3 = acos(cos_3p) + self.a435 - 90.0

        if abs(cos_2p) > 1:
            logger.debug('不能构成连杆结构, abs(cos_2p(%s)) > 1', cos_2p)
            return False
        rot_j2 = acos(cos_2p) + atan2(dis_ver_5_2, dis_hor_5_2)

        return {"rot_j1": rot_j1, "rot_j2": rot_j2, "rot_j3": rot_j3, "coordinate_5": (x0, y0, z0)}


if __name__ == '__main__':
    ik = IK()
    ik.setLinkLength()
    print('连杆长度：', ik.getLinkLength())
    print(ik.getJointsAngles((0, 0, 0), 0, 0))
