from sqlalchemy.orm import Session

from image import models
from image import schemas


# 获取所有的铁塔坐标集合
def get_point_tower(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.PointTower).offset(skip).limit(limit).all()


# 新建铁塔的坐标
def db_create_point_tower(db: Session, point_tower: schemas.PointTowerBase, tower_id: int):
    db_data = models.PointTower(**point_tower.dict(), tower_id=tower_id)
    db.add(db_data)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_data)  # 刷新
    return db_data
