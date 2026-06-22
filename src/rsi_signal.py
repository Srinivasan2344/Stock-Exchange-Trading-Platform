import pandas as pd

df = pd.read_csv("data/processed_stock_data.csv")

latest_rsi = df["RSI"].iloc[-1]

if latest_rsi < 30:
    signal = "BUY"
elif latest_rsi > 70:
    signal = "SELL"
else:
    signal = "HOLD"

print("RSI:", round(latest_rsi, 2))
print("Signal:", signal)