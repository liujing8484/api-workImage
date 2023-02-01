from fastapi import APIRouter, Depends, File
from sqlalchemy.orm import Session
import pandas as pd
from image.models import *
from typing import List

from image import crud
from image import schemas
from ..database import SessionLocal, engine, Base

app = APIRouter()

Base.metadata.create_all(bind=engine)  # 数据库初始化，如果没有库或者表，会自动创建


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 通过excel导入铁塔、塔间、控制点、引绳及导线、其他
@app.post("/excel_file/")
def create_models_from_excel(file: bytes = File(...), db: Session = Depends(get_db)):
    # 删除数据库
    db.query(PowerTower).delete()
    db.query(PowerAcross).delete()
    db.query(PowerBet).delete()
    db.query(Other).delete()
    db.query(Wire).delete()
    db.query(Across).delete()
    db.query(Bet).delete()
    db.query(Tower).delete()
    # tower
    data = pd.read_excel(file, sheet_name='towers', index_col=0)
    for row in data.itertuples():
        tower = {
            "tName": row.tName,
            "tType": row.tType,
            "tStyle": row.tStyle,
            "corner": row.corner,
            "altitude": row.altitude,
            "remark": row.remark
        }
        crud.db_create_tower(db=db, tower=schemas.CreateTower(**tower))
    # bet
    data_bet = pd.read_excel(file, sheet_name="bets", index_col=0)
    for row in data_bet.itertuples():
        # btName = row.btName
        # first_tower_name, after_tower_name = btName.split("--")
        # first_tower = crud.get_tower_by_name(db, first_tower_name)
        bet = {
            "btName": row.btName,
            "btSpan": row.btSpan,
            "remark": row.remark,
        }
        crud.db_create_bet(db=db, bet=schemas.CreateBet(**bet))
    # across
    data_across = pd.read_excel(file, sheet_name="across", index_col=0)
    for row in data_across.itertuples():
        btName = row.btName
        bet = crud.get_bet_by_name(db, btName)
        across = {
            "acrossName": row.acrossName,
            "acrossX": row.acrossX,
            "acrossY": row.acrossY,
            "controlHight": row.controlHight,
            "remark": row.remark,
        }
        crud.db_create_across(db=db, across=schemas.CreateAcross(**across), bet_id=bet.id)
    # wire
    data_wire = pd.read_excel(file, sheet_name="wires", index_col=0)
    for row in data_wire.itertuples():
        wire = {
            "wireName": row.wireName,
            "wireStyle": row.wireStyle,
            "wireWeight": row.wireWeight,
            "wirePower": row.wirePower,
            "remark": row.remark,
        }
        crud.db_create_wire(db=db, wire=schemas.CreateWire(**wire))
    # other
    data_other = pd.read_excel(file, sheet_name="others", index_col=0)
    for row in data_other.itertuples():
        other = {
            "otherName": row.otherName,
            "otherNum": row.otherNum,
            "remark": row.remark,
        }
        crud.db_create_other(db=db, other=schemas.CreateOther(**other))
    return {"message": "导入数据库成功"}


# 获取铁塔集合
@app.get("/get_towers/", response_model=List[schemas.Tower])
def get_towers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_towers(db=db, skip=skip, limit=limit)


# 获取塔间集合
@app.get("/get_bets/", response_model=List[schemas.Bet])
def get_bets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_bets(db=db, skip=skip, limit=limit)


# 获取控制点集合
@app.get("/get_across/", response_model=List[schemas.Across])
def get_across(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_across(db=db, skip=skip, limit=limit)


# 获取引绳和导线集合
@app.get("/get_wires/", response_model=List[schemas.Wire])
def get_wires(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_wires(db=db, skip=skip, limit=limit)


# 获取其他参数集合
@app.get("/get_others/", response_model=List[schemas.Other])
def get_others(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_others(db=db, skip=skip, limit=limit)
