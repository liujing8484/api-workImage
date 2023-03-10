from sqlalchemy.orm import Session

from image import models
from image import schemas


# 获取所有的塔间受力集合
def get_power_bet(db: Session, name: str = None, skip: int = 0, limit: int = 10):
    if name:
        return db.query(models.PowerBet).filter(models.PowerBet.bet.has(btName=name)).first()
    return db.query(models.PowerBet).offset(skip).limit(limit).all()


# 获取所有的控制点受力集合
def get_power_across(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.PowerAcross).offset(skip).limit(limit).all()


# 获取所有的控制点受力集合
def get_power_tower(db: Session, name: str = None, skip: int = 0, limit: int = 10):
    if name:
        return db.query(models.PowerTower).filter(models.PowerTower.tower.has(tName=name)).first()
    return db.query(models.PowerTower).offset(skip).limit(limit).all()


# 新建塔间的受力
def db_create_powerBet(db: Session, powerBet: schemas.PowerBetBase, bet_id: int):
    db_data = models.PowerBet(**powerBet.dict(), bet_id=bet_id)
    db.add(db_data)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_data)  # 刷新
    return db_data


# 新建塔间的受力
def db_create_powerAcross(db: Session, powerAcross: schemas.PowerAcrossBase, across_id: int):
    db_data = models.PowerAcross(**powerAcross.dict(), across_id=across_id)
    db.add(db_data)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_data)  # 刷新
    return db_data


# 新建铁塔的受力
def db_create_powerTower(db: Session, powerTower: schemas.PowerTowerBase, tower_id: int):
    db_data = models.PowerTower(**powerTower.dict(), tower_id=tower_id)
    db.add(db_data)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_data)  # 刷新
    return db_data
