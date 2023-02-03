from sqlalchemy import Column, Integer, Float, ForeignKey, String
# from sqlalchemy.dialects.postgresql import ARRAY
# from sqlalchemy import ARRAY
from ..database import Base
from sqlalchemy.orm import relationship


class PowerBet(Base):
    __tablename__ = "power_bet"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bet_id = Column(Integer, ForeignKey("bets.id"))
    h = Column(Float, nullable=False, comment='高差')
    angle = Column(Float, nullable=False, comment='高差角')

    bet = relationship("Bet", back_populates="powerbet")


class PowerAcross(Base):
    __tablename__ = "power_across"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    across_id = Column(Integer, ForeignKey("across.id"))
    hi = Column(Float, nullable=False, comment='水平张力')
    fi = Column(Float, nullable=False, comment='弧垂')
    fb = Column(Float, nullable=False, comment='平视弧垂')
    ti = Column(Float, nullable=False, comment='出口张力')

    across = relationship("Across")


class PowerTower(Base):
    __tablename__ = "power_tower"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tower_id = Column(Integer, ForeignKey("towers.id"))
    si = Column(Float, nullable=False, comment='牵引力')  # 走板通过此基塔滑车，牵引机的牵引力
    sis = Column(String(256))  # 走板通过此个滑车，每基塔的轴向张力集合

    tower = relationship("Tower")
