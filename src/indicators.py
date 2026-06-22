import pandas as pd

df = pd.read_csv("data/processed_stock_data.csv")

delta = df["Close"].diff()

gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)

avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss

df["RSI"] = 100 - (100 / (1 + rs))

df.to_csv("data/processed_stock_data.csv", index=False)

print(df[["Close", "RSI"]].tail())

exp1 = df["Close"].ewm(span=12, adjust=False).mean()
exp2 = df["Close"].ewm(span=26, adjust=False).mean()

df["MACD"] = exp1 - exp2
df["Signal_Line"] = df["MACD"].ewm(span=9, adjust=False).mean()