from .model import *
from typing import List


class PointTowerBase(BaseModel):
    x: float
    y: float


class PointTower(PointTowerBase):
    id: int
    tower: Tower

    class Config:
        orm_mode = True


class PointAcrossBase(BaseModel):
    x: float
    y: float


class PointAcross(PointAcrossBase):
    id: int
    across: Across

    class Config:
        orm_mode = True


class PointCurveBase(BaseModel):
    w: float
    xs: str
    ys: str
    index: int


class PointCurve(PointCurveBase):
    id: int
    bet: Bet

    class Config:
        orm_mode = True
