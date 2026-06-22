import yfinance as yf
import pandas as pd

ticker = "RELIANCE.NS"

data = yf.download(
    ticker,
    start="2020-01-01",
    end="2025-01-01",
    auto_adjust=True
)

# MultiIndex columns -> normal columns
data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]

data = data.reset_index()

print(data.columns)

data.to_csv("data/stock_data.csv", index=False)

print("Data Saved")