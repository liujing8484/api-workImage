import math


def getAngle(h, bt_span):
    """ 计算高差角 """
    return math.atan(h / bt_span)


def getHi(w, x, y, y1, bt_span, angle):
    """ 计算水平张力 """
    # x,y == 控制点的距离和高程
    # y1 == 前一基塔的高程
    return w * x * (bt_span - x) / 2 / ((y1 - y) * math.cos(angle) + x * math.sin(angle))


def getFi(bt_span, w, hi, angle):
    """ 计算弧垂 """
    return bt_span ** 2 * w / 8 / hi / math.cos(angle)


def getFB(fi, h):
    """ 计算平视弧垂 """
    return fi * (1 + h / 4 / fi) ** 2


def getSi(si, w, h, m, e):
    """ 计算牵引力
    si:前一基塔的si
    w:自重比载
    h：高差
    m：展放导线的数量
    """
    return (si + w * h * m) * e


def getHiFromTa(si0, w, h, bt_span, angle):
    """通过si计算Hi"""
    a = 1 + h ** 2 / 2 / bt_span ** 2
    b = w ** 2 / 8 / math.cos(angle) ** 2 - w * h / 2 / math.cos(angle)
    return (si0 + math.sqrt(si0 ** 2 - 4 * si0 * b)) / 2 / a


def getCurveXY(w, x, bt_span, lei_span, altitude, hi, angle):
    """ 获取曲线xy坐标"""
    fx = w * x * (bt_span - x) / 2 / hi / math.cos(angle)
    point_x = lei_span + x
    point_y = altitude + x * math.tan(angle) - fx
    return point_x, point_y
