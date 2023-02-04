from sqlalchemy import Column, Integer, Float, ForeignKey, String
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


class PointCurve(Base):
    __tablename__ = "point_curve"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bet_id = Column(Integer, ForeignKey("bets.id"))
    index = Column(Integer, nullable=False, comment='走板通过的塔位')
    w = Column(Float, nullable=False, comment='引绳自重')
    xs = Column(String(500))  # x坐标的集合
    ys = Column(String(500))  # y坐标的集合

    bet = relationship("Bet")
