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


# 所有的点都会通过这个方法
def getXY(x, y):
    return {
        "x": x / 2,
        "y": y * 5
    }


@app.get("/calculate_point/")
def calculate_point(db: Session = Depends(get_db)):
    towers = db.query(models.Tower).all()
    bets = db.query(models.Bet).all()
    lst_across = db.query(models.Across).all()

    # 计算tower的坐标
    db.query(models.PointTower).delete()
    lei = 0
    for tower, bet in zip(towers, bets):
        point_tower = getXY(lei, tower.altitude)
        lei += bet.btSpan
        crud.db_create_point_tower(db, point_tower=schemas.PointTowerBase(**point_tower), tower_id=tower.id)
    else:
        point_tower = getXY(lei, towers[-1].altitude)
        crud.db_create_point_tower(db, point_tower=schemas.PointTowerBase(**point_tower), tower_id=towers[-1].id)

    # 计算across的坐标
    for across in lst_across:
        bet = across.bet
        bets_new = filter(lambda b: b.id < bet.id, bets)
        x = sum(map(lambda b: b.btSpan, bets_new)) + across.acrossX
        y = across.acrossY
        point_across = getXY(x, y)
        crud.db_create_point_across(db, schemas.PointAcrossBase(**point_across), across_id=across.id)

    # 计算curve的坐标

    return {"message": "坐标计算成功"}


@app.post("/calculate_point_curve")
def calculate_point_curve(param: schemas.CalculateCurveParam, db: Session = Depends(get_db)):
    bets = db.query(models.Bet).all()

    for bet in bets:
        tName, _ = bet.btName.split("--")
        tower = crud.get_tower_by_name(db, name=tName)
        power_bet = crud.get_power_bet(db, name=bet.btName)
        h, angle = power_bet.h, power_bet.angle
        bt_span = bet.btSpan
        lei_span = power_bet.leiSpan
        altitude = tower.altitude

        # hi = getHiFromTa(si0, w, h, bt_span, angle)  # 先计算水平力
        #
        # points = []
        # for index in range(50):
        #     x = bt_span / 49 * index
        #     point_x, point_y = getCurveXY(param.w_d, x, bt_span, lei_span, altitude, hi, angle)


# 获取铁塔点坐标集合
@app.get("/get_point_towers/", response_model=List[schemas.PointTower])
def get_point_towers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_point_tower(db=db, skip=skip, limit=limit)


# 获取控制点坐标集合
@app.get("/get_point_across/", response_model=List[schemas.PointAcross])
def get_point_across(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_point_across(db=db, skip=skip, limit=limit)
