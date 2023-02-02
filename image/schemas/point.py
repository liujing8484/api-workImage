from .model import *


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
