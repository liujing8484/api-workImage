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


@app.get("/calculate")
def calculate(db: Session = Depends(get_db)):
    # power_bet
    bets = db.query(models.Bet).all()
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

    return {"message": "受力计算成功"}


# 获取塔间集合
@app.get("/get_power_bets/", response_model=List[schemas.PowerBet])
def get_power_bets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_power_bets(db=db, skip=skip, limit=limit)
