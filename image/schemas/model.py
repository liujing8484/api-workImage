from pydantic import BaseModel


class CreateTower(BaseModel):
    tName: str
    tType: str
    tStyle: str
    corner: str
    altitude: float
    remark: str


class Tower(CreateTower):
    id: int

    class Config:
        orm_mode = True


class BetBase(BaseModel):
    btName: str
    btSpan: int
    remark: str


class CreateBet(BetBase):
    pass


class Bet(BetBase):
    id: int

    # first_tower: Tower

    class Config:
        orm_mode = True


class AcrossBase(BaseModel):
    acrossName: str
    acrossX: float
    acrossY: float
    controlHight: float
    remark: str


class CreateAcross(AcrossBase):
    pass


class Across(AcrossBase):
    id: int
    bet: Bet

    class Config:
        orm_mode = True


# wire
class WireBase(BaseModel):
    wireName: str
    wireStyle: str
    wireWeight: float
    wirePower: float
    remark: str


class CreateWire(WireBase):
    pass


class Wire(WireBase):
    id: int

    class Config:
        orm_mode = True


# other
class OtherBase(BaseModel):
    otherName: str
    otherNum: float
    remark: str


class CreateOther(OtherBase):
    pass


class Other(OtherBase):
    id: int

    class Config:
        orm_mode = True


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


class PowerTower(PowerTowerBase):
    id: int
    tower: Tower

    class Config:
        orm_mode = True