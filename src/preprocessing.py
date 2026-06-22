import pandas as pd

df = pd.read_csv("data/stock_data.csv", skiprows=3)

df.columns = ["Date", "Close", "High", "Low", "Open", "Volume"]

for col in ["Close", "High", "Low", "Open", "Volume"]:
    df[col] = pd.to_numeric(df[col])

df["MA10"] = df["Close"].rolling(10).mean()
df["MA20"] = df["Close"].rolling(20).mean()
df["Return"] = df["Close"].pct_change()
df["Target"] = df["Close"].shift(-1)

df = df.dropna()

df.to_csv("data/processed_stock_data.csv", index=False)

print(df.head())
print("Preprocessing completed")