from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


class Tower(Base):
    __tablename__ = "towers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tName = Column(String(50), unique=True, nullable=False, comment='塔名')
    tType = Column(String(50), nullable=False, comment='塔型')
    tStyle = Column(String(50), nullable=False, comment='塔类')
    corner = Column(String(50), comment='转角')
    altitude = Column(Float, nullable=False, comment='高程')
    remark = Column(String(50), comment='备注')

    # bet = relationship("Bet", back_populates="first_tower")
    # bet_after_tower = relationship("Bet", back_populates="after_tower")


class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    btName = Column(String(50), unique=True, nullable=False, comment='塔间名')
    btSpan = Column(Integer, nullable=False, comment="档距")
    # first_tower_id = Column(Integer, ForeignKey("towers.id"))
    # after_tower_id = Column(Integer, ForeignKey("towers.id"))
    remark = Column(String(50), comment='备注')

    # first_tower = relationship("Tower", back_populates="bet")
    # after_tower = relationship("Tower")
    across = relationship("Across", back_populates="bet")


class Across(Base):
    __tablename__ = "across"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bet_id = Column(Integer, ForeignKey("bets.id"))
    acrossName = Column(String(50), comment='跨越点')
    acrossX = Column(Float, nullable=False, comment='X')
    acrossY = Column(Float, nullable=False, comment='Y')
    controlHight = Column(Float, nullable=False, comment='控制距离')
    remark = Column(String(50), comment='备注')

    bet = relationship("Bet", back_populates="across")


class Wire(Base):
    __tablename__ = "wires"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    wireName = Column(String(50), comment='名称')
    wireStyle = Column(String(50), comment='型号')
    wireWeight = Column(Float, nullable=False, comment='自重')
    wirePower = Column(Float, default=0, comment='自重')
    remark = Column(String(50), comment='备注')


class Other(Base):
    __tablename__ = "others"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    otherName = Column(String(50), comment='名称')
    otherNum = Column(Float, nullable=False, comment='数值')
    remark = Column(String(50), comment='备注')


class power_bet(Base):
    __tablename__ = "power_bet"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bet_id = Column(Integer, ForeignKey("bets.id"))
    h = Column(Float, nullable=False, comment='高差')
    angle = Column(Float, nullable=False, comment='高差角')

    bet = relationship("Bet")


class power_across(Base):
    __tablename__ = "power_across"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    across_id = Column(Integer, ForeignKey("across.id"))
    hi = Column(Float, nullable=False, comment='水平张力')
    fi = Column(Float, nullable=False, comment='弧垂')
    fb = Column(Float, nullable=False, comment='平视弧垂')
    ti = Column(Float, nullable=False, comment='出口张力')

    across = relationship("Across", back_populates="across")


class power_tower(Base):
    __tablename__ = "power_tower"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tower_id = Column(Integer, ForeignKey("towers.id"))
    si = Column(Float, nullable=False, comment='牵引力')

    tower = relationship("Tower")
