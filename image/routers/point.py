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
    lst_sis = [p.sis for p in db.query(models.PowerTower).all()]
    # 假定走板通过id的塔位，那么可以求的每基塔位的牵引力
    lst_s = json.loads(lst_sis[param.index])
    # 那么就可以计算所有点坐标的集合
    length = len(bets)
    for index_bet, bet in enumerate(bets):
        if index_bet <= param.index:
            w = param.w_d
            # lst_points.append(cal_points_bet_single(db, w, lst_s, index_bet))
        else:
            w = param.w_p
            # lst_points.append(cal_points_bet_single(db, w, lst_s, index_bet))
        xs, ys = cal_points_bet_single(db, w, lst_s, index_bet)
        point_curve = {
            "w": w,
            "xs": json.dumps(xs),
            "ys": json.dumps(ys),
        }
        crud.db_create_point_curve(db, schemas.PointCurveBase(**point_curve), bet_id=bet.id)
    return {"message": "坐标计算成功"}


# 计算单段曲线坐标点
def cal_points_bet_single(db, w, powers, index):
    bet = db.query(models.Bet).all()[index]
    tName, _ = bet.btName.split("--")
    tower = crud.get_tower_by_name(db, name=tName)
    power_bet = crud.get_power_bet(db, name=bet.btName)
    h, angle = power_bet.h, power_bet.angle
    bt_span = bet.btSpan
    lei_span = power_bet.lei_span
    altitude = tower.altitude

    si0 = powers[index]
    hi = getHiFromTa(si0, w, h, bt_span, angle)  # 先计算水平力

    lst_x = []
    lst_y = []
    for i in range(50):
        x = bt_span / 49 * i
        point_x, point_y = getCurveXY(w, x, bt_span, lei_span, altitude, hi, angle)
        p_x, p_y = getXY(point_x, point_y)
        lst_x.append(p_x)
        lst_y.append(p_y)

    return lst_x, lst_y


# 获取铁塔点坐标集合
@app.get("/get_point_towers/", response_model=List[schemas.PointTower])
def get_point_towers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_point_tower(db=db, skip=skip, limit=limit)


# 获取控制点坐标集合
@app.get("/get_point_across/", response_model=List[schemas.PointAcross])
def get_point_across(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_point_across(db=db, skip=skip, limit=limit)
