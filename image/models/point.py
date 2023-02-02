from sqlalchemy import Column, Integer, String, Float, ForeignKey
from ..database import Base
from sqlalchemy.orm import relationship


class PointTower(Base):
    __tablename__ = "point_tower"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tower_id = Column(Integer, ForeignKey("towers.id"))
    x = Column(Float, nullable=False, comment='x')
    y = Column(Float, nullable=False, comment='y')

    tower = relationship("Tower")


class PointAcross(Base):
    __tablename__ = "point_across"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    across_id = Column(Integer, ForeignKey("across.id"))
    x = Column(Float, nullable=False, comment='x')
    y = Column(Float, nullable=False, comment='y')

    across = relationship("Across")
