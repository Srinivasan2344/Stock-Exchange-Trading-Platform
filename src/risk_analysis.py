import pandas as pd

df = pd.read_csv("data/processed_stock_data.csv")

returns = df["Return"]

volatility = returns.std() * (252 ** 0.5)

max_drawdown = (
    (df["Close"] / df["Close"].cummax()) - 1
).min()

print(f"Annualized Volatility: {volatility:.4f}")
print(f"Maximum Drawdown: {max_drawdown:.4f}")