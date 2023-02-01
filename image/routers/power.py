from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from image import models, crud, schemas
from ..database import SessionLocal
from ..utils import *

app = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 计算ti
def cal_ti(a, w, e, lst_h):
    lst_h.reverse()
    ti = a
    for h in lst_h:
        ti = ti / e - w * h
    return ti


@app.get("/calculate/{w}")
def calculate(w: float = 3.01, db: Session = Depends(get_db)):
    # power_bet
    bets = db.query(models.Bet).all()
    db.query(models.PowerBet).delete()
    for bet in bets:
        tName1, tName2 = bet.btName.split("--")
        tower1 = crud.get_tower_by_name(db, tName1)
        tower2 = crud.get_tower_by_name(db, tName2)
        h = tower2.altitude - tower1.altitude
        angle = getAngle(h, bet.btSpan)
        power_bet = {
            "h": h,
            "angle": angle
        }
        crud.db_create_powerBet(db, powerBet=schemas.PowerBetBase(**power_bet), bet_id=bet.id)
    # power_across
    lst_power_bet = db.query(models.PowerBet).all()
    lst_across = db.query(models.Across).all()
    for across in lst_across:
        print("*" * 20, across.__dict__)
        x, y = across.acrossX, across.acrossY + across.controlHight
        bet = across.bet
        tName, _ = bet.btName.split("--")
        tower = crud.get_tower_by_name(db, tName)
        power_bet = crud.get_power_bet(db, name=bet.btName)
        y1 = tower.altitude
        btSpan = bet.btSpan
        h = power_bet.h
        angle = power_bet.angle
        hi = getHi(w, x, y, y1, btSpan, angle)
        fi = getFi(btSpan, w, hi, angle)
        fb = getFB(fi, h)
        ti_a = hi + w / math.cos(angle) * fb - w * h
        lst_h = list(map(lambda p: p.h, filter(lambda b: b.id < power_bet.id, lst_power_bet)))
        ti = cal_ti(ti_a, w, 1.015, lst_h)
        power_across = {
            "hi": hi,
            "fi": fi,
            "fb": fb,
            "ti": ti,
        }
        crud.db_create_powerAcross(db, schemas.PowerAcrossBase(**power_across), across_id=across.id)
    # power_tower

    return {"message": "受力计算成功"}


# 获取塔间受力集合
@app.get("/get_power_bets/", response_model=List[schemas.PowerBet])
def get_power_bets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_power_bet(db=db, skip=skip, limit=limit)


# 获取控制点受力集合
@app.get("/get_power_across/", response_model=List[schemas.PowerAcross])
def get_power_across(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_power_across(db=db, skip=skip, limit=limit)
