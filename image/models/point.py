from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
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

#
# class PointCurve(Base):
#     __tablename__ = "point_curve"
#
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     bet_id = Column(Integer, ForeignKey("across.id"))
#     xs = Column(ARRAY(Float))  # x左边的集合
#     ys = Column(ARRAY(Float))  # y坐标的集合
#
#     bet = relationship("Bet")
