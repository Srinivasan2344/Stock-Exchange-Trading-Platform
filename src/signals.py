import pandas as pd

df = pd.read_csv("data/processed_stock_data.csv")

latest = df.iloc[-1]

if latest["MA10"] > latest["MA20"]:
    signal = "BUY"
elif latest["MA10"] < latest["MA20"]:
    signal = "SELL"
else:
    signal = "HOLD"

print("Signal:", signal)