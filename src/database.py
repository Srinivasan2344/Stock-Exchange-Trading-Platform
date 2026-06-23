import streamlit as st
import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine

st.set_page_config(
    page_title="AI Stock Trading Dashboard",
    layout="wide"
)

st.title("📈 AI Stock Trading Dashboard")

# -----------------------------
# Load Processed Data
# -----------------------------

try:
    df = pd.read_csv("data/processed_stock_data.csv")

    latest = df.iloc[-1]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Close Price",
        round(latest["Close"], 2)
    )

    col2.metric(
        "MA10",
        round(latest["MA10"], 2)
    )

    col3.metric(
        "MA20",
        round(latest["MA20"], 2)
    )

    st.subheader("Stock Price Trend")

    st.line_chart(
        df.set_index("Date")["Close"]
    )

    st.subheader("Moving Averages")

    st.line_chart(
        df.set_index("Date")[["Close", "MA10", "MA20"]]
    )

    returns = df["Return"]

    volatility = returns.std() * (252 ** 0.5)

    cumulative_returns = (1 + returns).cumprod()

    rolling_max = cumulative_returns.cummax()

    drawdown = (
        cumulative_returns - rolling_max
    ) / rolling_max

    max_drawdown = drawdown.min()

    st.subheader("Risk Metrics")

    c1, c2 = st.columns(2)

    c1.metric(
        "Annualized Volatility",
        f"{volatility:.2%}"
    )

    c2.metric(
        "Maximum Drawdown",
        f"{max_drawdown:.2%}"
    )

except Exception as e:
    st.warning(f"Processed Data Not Found: {e}")

# -----------------------------
# Live Stock Analysis
# -----------------------------

st.subheader("Live Stock Analysis")

stock = st.selectbox(
    "Select Stock",
    [
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS",
        "HDFCBANK.NS"
    ]
)

if st.button("Load Data"):

    live_df = yf.download(
        stock,
        start="2020-01-01",
        progress=False
    )

    st.success("Data Loaded Successfully")

    st.line_chart(
        live_df["Close"]
    )

# -----------------------------
# Stock Comparison
# -----------------------------

st.subheader("Stock Comparison")

comparison = pd.DataFrame()

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS"
]

for ticker in stocks:

    data = yf.download(
        ticker,
        start="2024-01-01",
        progress=False
    )

    comparison[ticker] = data["Close"]

st.line_chart(comparison)

# -----------------------------
# PostgreSQL Portfolio
# -----------------------------

st.subheader("Portfolio Holdings")

try:

    engine = create_engine(
        "postgresql://postgres:durai123@localhost:5432/stock_trading"
    )

    portfolio_df = pd.read_sql(
        "SELECT * FROM portfolio",
        engine
    )

    st.dataframe(portfolio_df)

except Exception as e:

    st.warning(
        f"Portfolio Table Error: {e}"
    )

# -----------------------------
# Trade History
# -----------------------------

st.subheader("Trade History")

try:

    trade_df = pd.read_sql(
        "SELECT * FROM trade_history",
        engine
    )

    st.dataframe(trade_df)

except Exception as e:

    st.warning(
        f"Trade History Error: {e}"
    )

st.success("Dashboard Loaded Successfully")

