import pandas as pd
import numpy as np
import yfinance as yf

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS"
]

data = yf.download(
    stocks,
    start="2024-01-01",
    auto_adjust=True,
    progress=False
)["Close"]

returns = data.pct_change().dropna()

weights = np.array([0.25, 0.25, 0.25, 0.25])

portfolio_return = np.sum(
    returns.mean() * weights
) * 252

portfolio_risk = np.sqrt(
    np.dot(
        weights.T,
        np.dot(
            returns.cov() * 252,
            weights
        )
    )
)

print("Expected Annual Return:", round(portfolio_return, 4))
print("Portfolio Risk:", round(portfolio_risk, 4))