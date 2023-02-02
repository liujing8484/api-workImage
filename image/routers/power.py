import json

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


# 走板过第index塔位时受力si
def cal_si(index, param, ti_max, db):
    lst_h = [p.h for p in db.query(models.PowerBet).all()]
    si = ti_max
    lst_si = []
    for i, h in enumerate(lst_h):
        if i < index:
            si = getSi(si, param.w_d, h, param.num, param.e)
            lst_si.append(si)
        else:
            si = getSi(si, param.w_p, h, 1, param.e)
            lst_si.append(si)
    return si, json.dumps(lst_si)


@app.post("/calculate/")
def calculate_power(param: schemas.CalculatePowerParam, db: Session = Depends(get_db)):
    # power_bet
    bets = db.query(models.Bet).all()
    towers = db.query(models.Tower).all()
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
    w = param.w_d  # 导引绳的自重
    for across in lst_across:
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
    # 获取最大的ti
    ti_max = max(db.query(models.PowerAcross).all(), key=lambda p: p.ti).ti
    # power_tower
    db.query(models.PowerTower).delete()  # 将power_tower的值全部删除
    for index, tower in enumerate(towers):
        si, lst_si = cal_si(index, param, ti_max, db)
        power_tower = {
            "si": si,
            "sis": lst_si
        }
        crud.db_create_powerTower(db, powerTower=schemas.PowerTowerBase(**power_tower), tower_id=tower.id)
    return {"message": "受力计算成功"}


# 获取塔间受力集合
@app.get("/get_power_bets/", response_model=List[schemas.PowerBet])
def get_power_bets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_power_bet(db=db, skip=skip, limit=limit)


# 获取控制点受力集合
@app.get("/get_power_across/", response_model=List[schemas.PowerAcross])
def get_power_across(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_power_across(db=db, skip=skip, limit=limit)


# 获取控制点受力集合
@app.get("/get_power_tower/", response_model=List[schemas.PowerTower])
def get_power_tower(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_power_tower(db=db, skip=skip, limit=limit)
