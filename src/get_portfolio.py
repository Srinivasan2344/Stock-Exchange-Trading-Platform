from database import SessionLocal
from models import Portfolio

session = SessionLocal()

portfolio = session.query(Portfolio).all()

for stock in portfolio:
    print(
        stock.stock,
        stock.quantity,
        stock.buy_price
    )

session.close()