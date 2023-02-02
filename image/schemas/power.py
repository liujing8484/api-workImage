from .model import *
from typing import List


class PowerBetBase(BaseModel):
    h: float
    angle: float


class PowerBet(PowerBetBase):
    id: int
    bet: Bet

    class Config:
        orm_mode = True


class PowerAcrossBase(BaseModel):
    hi: float
    fi: float
    fb: float
    ti: float


class PowerAcross(PowerAcrossBase):
    id: int
    across: Across

    class Config:
        orm_mode = True


class PowerTowerBase(BaseModel):
    si: float
    sis: str


class PowerTower(PowerTowerBase):
    id: int
    tower: Tower

    class Config:
        orm_mode = True
