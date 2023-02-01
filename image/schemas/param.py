from pydantic import BaseModel


class CalculatePowerParam(BaseModel):
    w_p: float = 0.8
    w_d: float = 3.01
    num: int = 1
    e: float = 1.015
