from sqlalchemy.orm import Session

from image import models
from image import schemas


# 通过id查询铁塔
def get_tower(db: Session, tower_id: int):
    return db.query(models.Tower).filter(models.Tower.id == tower_id).first()


# 获取所有的铁塔集合
def get_towers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Tower).offset(skip).limit(limit).all()


# 获取所有的塔间集合
def get_bets(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Bet).offset(skip).limit(limit).all()


# 获取所有的控制点集合
def get_across(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Across).offset(skip).limit(limit).all()


# 获取所有的引绳和导线集合
def get_wires(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Wire).offset(skip).limit(limit).all()


# 获取所有的其他参数集合
def get_others(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Other).offset(skip).limit(limit).all()


# 获取所有的塔间受力集合
def get_power_bet(db: Session, name: str = None, skip: int = 0, limit: int = 10):
    if name:
        return db.query(models.PowerBet).filter(models.PowerBet.bet.has(btName=name)).first()
    return db.query(models.PowerBet).offset(skip).limit(limit).all()


# 获取所有的控制点受力集合
def get_power_across(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.PowerAcross).offset(skip).limit(limit).all()


# 获取所有的控制点受力集合
def get_power_tower(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.PowerTower).offset(skip).limit(limit).all()


# 通过名称查询铁塔
def get_tower_by_name(db: Session, name: str):
    return db.query(models.Tower).filter(models.Tower.tName == name).first()


# 新建铁塔
def db_create_tower(db: Session, tower: schemas.CreateTower):
    db_data = models.Tower(**tower.dict())
    db.add(db_data)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_data)  # 刷新
    return db_data


# 通过名称查询铁塔
def get_bet_by_name(db: Session, name: str):
    return db.query(models.Bet).filter(models.Bet.btName == name).first()


# 新建塔间
def db_create_bet(db: Session, bet: schemas.CreateBet):
    db_data = models.Bet(**bet.dict())
    db.add(db_data)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_data)  # 刷新
    return db_data


# 新建控制点
def db_create_across(db: Session, across: schemas.CreateAcross, bet_id: int):
    db_data = models.Across(**across.dict(), bet_id=bet_id)
    db.add(db_data)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_data)  # 刷新
    return db_data


# 新建引绳及导线
def db_create_wire(db: Session, wire: schemas.CreateWire):
    db_data = models.Wire(**wire.dict())
    db.add(db_data)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_data)  # 刷新
    return db_data


# 新建其他参数
def db_create_other(db: Session, other: schemas.CreateOther):
    db_data = models.Other(**other.dict())
    db.add(db_data)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_data)  # 刷新
    return db_data


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
