from pydantic import BaseModel


class CalculatePowerParam(BaseModel):
    w_p: float = 0.8
    w_d: float = 3.01
    num: int = 1
    e: float = 1.015


class CalculateCurveParam(BaseModel):
    direction: bool = True  # true:向大号侧；false:向小号侧
    Site: int = 0  # 1:大牵张;0:小牵张
    w_p: float = 0.8  # 牵引绳自重
    w_d: float = 3.01  # 导引绳自重
    num: int = 1  # 展放数量
    e: float = 1.015
    index: int = 0  # 走板通过的塔位的index
