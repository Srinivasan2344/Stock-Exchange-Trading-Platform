from sqlalchemy.orm import sessionmaker
from database import engine
from models import Portfolio

Session = sessionmaker(bind=engine)
session = Session()

portfolio = Portfolio(
    stock="RELIANCE.NS",
    quantity=10,
    buy_price=1500
)

session.add(portfolio)
session.commit()

print("Portfolio Saved Successfully")

session.close()