from sqlalchemy.orm import Session

from image import models
from image import schemas


# 获取所有的铁塔坐标集合
def get_point_tower(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.PointTower).offset(skip).limit(limit).all()


# 获取所有的控制点坐标集合
def get_point_across(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.PointAcross).offset(skip).limit(limit).all()


# 获取所有的控制点坐标集合
def get_point_curve(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.PointCurve).offset(skip).limit(limit).all()


# 新建铁塔的坐标
def db_create_point_tower(db: Session, point_tower: schemas.PointTowerBase, tower_id: int):
    db_data = models.PointTower(**point_tower.dict(), tower_id=tower_id)
    db.add(db_data)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_data)  # 刷新
    return db_data


# 新建控制点的坐标
def db_create_point_across(db: Session, point_across: schemas.PointAcrossBase, across_id: int):
    db_data = models.PointAcross(**point_across.dict(), across_id=across_id)
    db.add(db_data)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_data)  # 刷新
    return db_data


# 新建曲线点的坐标
def db_create_point_curve(db: Session, point_curve: schemas.PointCurveBase, bet_id: int):
    db_data = models.PointCurve(**point_curve.dict(), bet_id=bet_id)
    db.add(db_data)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_data)  # 刷新
    return db_data
