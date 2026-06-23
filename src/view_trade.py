from sqlalchemy.orm import sessionmaker
from database import engine
from models import TradeHistory

Session = sessionmaker(bind=engine)
session = Session()

trades = session.query(TradeHistory).all()

for t in trades:
    print(
        t.id,
        t.stock,
        t.action,
        t.quantity,
        t.price
    )

session.close()