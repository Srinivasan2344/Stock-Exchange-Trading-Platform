from sqlalchemy import create_engine
from models import Base

engine = create_engine(
    "postgresql://postgres:durai123@localhost:5432/stock_trading"
)

Base.metadata.create_all(engine)

print("Tables Created")