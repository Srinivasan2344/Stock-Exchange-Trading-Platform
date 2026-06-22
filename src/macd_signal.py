import pandas as pd

df = pd.read_csv("data/processed_stock_data.csv")

latest = df.iloc[-1]

if latest["MACD"] > latest["Signal_Line"]:
    signal = "BUY"
else:
    signal = "SELL"

print("MACD Signal:", signal)