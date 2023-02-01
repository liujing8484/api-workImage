from .model import *


class PointTowerBase(BaseModel):
    x: float
    y: float


class PointTower(PointTowerBase):
    id: int
    tower: Tower

    class Config:
        orm_mode = True
