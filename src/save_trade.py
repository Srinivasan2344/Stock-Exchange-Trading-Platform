from database import SessionLocal
from models import TradeHistory

session = SessionLocal()

trade = TradeHistory(
    stock="TCS.NS",
    action="BUY",
    quantity=5,
    price=3500
)

session.add(trade)
session.commit()

print("Trade Saved Successfully")

session.close()