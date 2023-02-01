from fastapi import APIRouter, Depends
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


@app.get("/calculate_point/")
def calculate_point(db: Session = Depends(get_db)):
    towers = db.query(models.Tower).all()
    bets = db.query(models.Bet).all()

    # 计算tower的坐标
    lei = 0
    for tower, bet in zip(towers, bets):
        point_tower = {
            "x": tower.altitude,
            "y": lei
        }
        lei += bet.btSpan
        crud.db_create_point_tower(db, point_tower=schemas.PointTowerBase(**point_tower), tower_id=tower.id)
    else:
        point_tower = {
            "x": towers[-1].altitude,
            "y": lei
        }
        crud.db_create_point_tower(db, point_tower=schemas.PointTowerBase(**point_tower), tower_id=towers[-1].id)

    return {"message": "坐标计算成功"}


# 获取塔间受力集合
@app.get("/get_point_towers/", response_model=List[schemas.PointTower])
def get_point_towers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_point_tower(db=db, skip=skip, limit=limit)
