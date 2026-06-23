from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Portfolio(Base):
    __tablename__ = "portfolio"

    id = Column(Integer, primary_key=True)
    stock = Column(String)
    quantity = Column(Integer)
    buy_price = Column(Float)

class TradeHistory(Base):
    __tablename__ = "trade_history"

    id = Column(Integer, primary_key=True)
    stock = Column(String)
    action = Column(String)
    quantity = Column(Integer)
    price = Column(Float)