from sqlalchemy.orm import sessionmaker
from database import engine
from models import Portfolio

Session = sessionmaker(bind=engine)
session = Session()

records = session.query(Portfolio).all()

if records:
    for r in records:
        print(
            f"ID: {r.id}, "
            f"Stock: {r.stock}, "
            f"Quantity: {r.quantity}, "
            f"Buy Price: {r.buy_price}"
        )
else:
    print("No portfolio records found.")

session.close()