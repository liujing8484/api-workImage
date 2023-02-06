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
    controlHeight: float
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
