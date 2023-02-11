from sqlalchemy.orm import Session

from image import models
from image import schemas


# 获取所有的铁塔坐标集合
def get_point_tower(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.PointTower).offset(skip).limit(limit).all()


# 获取所有的控制点坐标集合
def get_point_across(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.PointAcross).offset(skip).limit(limit).all()


# 获取所有的控制点坐标集合(通过across)
def get_point_across_by_across(db: Session, across: schemas.Across):
    return db.query(models.PointAcross).filter(models.PointAcross.across == across)


# 获取所有的控制点坐标集合
def get_point_curve(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.PointCurve).offset(skip).limit(limit).all()


# 获取所有的控制点坐标集合
def get_min_max_xy(db: Session, name: str):
    return db.query(models.SizeData).filter(models.SizeData.name == name).first()


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


# 存储xy的最大值和最小值
def db_create_min_max_xy(db: Session, size: schemas.SizeDateBase):
    db_data = models.SizeData(**size.dict())
    db.add(db_data)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_data)  # 刷新
    return db_data
