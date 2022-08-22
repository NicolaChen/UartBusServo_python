import logging
from math import *

# CRITICAL, ERROR, WARNING, INFO, DEBUG
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class IK:
    # 舵机从下往上数
    # 公用参数，三维图纸测量获得，单位为mm和deg
    h1b = 118.16  # 一号舵机到水平底面到距离
    a210 = 45.86  # l12与水平面的夹角
    l12 = 65.49  # 底盘中心到二号舵机的距离
    l23 = 183.01  # 二号舵机到三号舵机的距离
    l35 = 318.62  # 三号舵机到五号舵机的连线距离
    a435 = 81.98  # 四号关节处定向线与l35连线到夹角
    l5s = 33.95  # 五号舵机到气动夹爪中心到距离

    def __init__(self):
        pass

    def setLinkLength(self, h_1b=h1b, a_210=a210, l_12=l12, l_23=l23, l_35=l35, l_5s=l5s, a_435=a435):
        self.h1b = h_1b
        self.a210 = a_210
        self.l12 = l_12
        self.l23 = l_23
        self.l35 = l_35
        self.l5s = l_5s
        self.a435 = a_435

    def getLinkLength(self):

        return {"h1b": self.h1b, "l12": self.l12, "a210": self.a210, "l23": self.l23, "l35": self.l35,
                "a435": self.a435, "l5s": self.l5s}

    # 给定指定坐标和末端所需4、5关节转角，返回每个关节应该旋转的角度，如果无解返回False
    # coordinate为夹爪末端中心坐标，坐标单位mm， 以元组形式传入，例如(0, 5, 10)
    # 设夹持器末端为end(X, Y, Z), 坐标原点为origin(0, 0, 0), 原点为底盘转盘中心在台面的投影， end点在地面的投影为end_p
    # 空间坐标轴放置标准：初始零位下，关节1与工作区中心连线为x轴，臂主体位于ZX平面，z轴垂直与工作平面向上；平面内逆时针旋转角度为正

    def getJointsAngles(self, coordinate_s, rot_ox, rot_oy):
        x, y, z = coordinate_s
        rad_ox = radians(rot_ox)
        rad_oy = radians(rot_oy)
        x0 = x - self.l5s * sin(rad_oy)
        y0 = y - self.l5s * cos(rad_oy) * cos(rad_ox)
        z0 = z + self.l5s * cos(rad_oy) * sin(rad_ox)

        rot_j1 = degrees(atan2(y0, x0))  # 求底座旋转角度
        dis_hor_5_2 = sqrt(x0 ** 2 + y0 ** 2) - self.l12 * cos(radians(self.a210))  # end_p到关节2的水平距离
        dis_ver_5_2 = z0 - self.l12 * sin(radians(self.a210)) - self.h1b  # end_p到关节2到垂直距离

        if self.l23 + self.l35 < sqrt(dis_hor_5_2 ** 2 + dis_ver_5_2 ** 2):  # 两边之和小于第三边
            logger.debug('不能构成连杆结构, l23(%s) + l35sin(%s) < AC(%s)', self.l23, self.l35,
                         sqrt(dis_hor_5_2 ** 2 + dis_ver_5_2 ** 2))
            return False

        cos_532 = (self.l23 ** 2 + self.l35 ** 2 - dis_ver_5_2 ** 2 - dis_hor_5_2 ** 2) / (2 * self.l23 * self.l35)
        cos_523 = (self.l23 ** 2 + dis_ver_5_2 ** 2 + dis_hor_5_2 ** 2 - self.l35 ** 2) / \
                  (2 * self.l23 * sqrt(dis_hor_5_2 ** 2 + dis_ver_5_2 ** 2))
        a520 = atan2(dis_ver_5_2, -1 * dis_hor_5_2)
        if a520 < 0:
            a520 += 2 * pi
        if abs(cos_523) > 1:
            logger.debug('不能构成连杆结构, abs(cos_532(%s)) > 1', cos_523)
            return False
        rot_j2 = degrees(a520 - acos(cos_523))
        rot_j3 = 270 - degrees(acos(cos_532)) - self.a435
        rot_j4 = rot_ox
        rot_j5 = rot_oy + 90 - (rot_j2 + rot_j3)

        return {"rot_j1": rot_j1, "rot_j2": rot_j2, "rot_j3": rot_j3, "rot_j4": rot_j4, "rot_j5": rot_j5,
                "coordinate_5": (x0, y0, z0)}  # 暂时使用同轴型末端夹具，故暂不考虑rot_j6的影响
