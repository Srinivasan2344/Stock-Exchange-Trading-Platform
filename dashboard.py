import streamlit as st
import pandas as pd
import yfinance as yf
import joblib

st.set_page_config(
    page_title="AI Stock Trading Dashboard",
    layout="wide"
)


# LOAD DATA

df = pd.read_csv("data/processed_stock_data.csv")

model = joblib.load("models/xgboost_model.pkl")

st.title(" AI Stock Trading Dashboard")


# LATEST METRICS

latest = df.iloc[-1]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Close Price",
    f"₹{latest['Close']:.2f}"
)

col2.metric(
    "MA10",
    f"₹{latest['MA10']:.2f}"
)

col3.metric(
    "MA20",
    f"₹{latest['MA20']:.2f}"
)

# PRICE TREND

st.subheader(" Stock Price Trend")

st.line_chart(
    df.set_index("Date")["Close"]
)

# MOVING AVERAGES

st.subheader(" Moving Averages")

st.line_chart(
    df.set_index("Date")[
        ["Close", "MA10", "MA20"]
    ]
)

# RECENT DATA

st.subheader("📋 Recent Data")

st.dataframe(df.tail())


# RISK ANALYTICS

returns = df["Return"]

volatility = returns.std() * (252 ** 0.5)

cumulative = (1 + returns).cumprod()

running_max = cumulative.cummax()

drawdown = (
    cumulative - running_max
) / running_max

max_drawdown = drawdown.min()

st.subheader("⚠ Risk Metrics")

col4, col5 = st.columns(2)

col4.metric(
    "Annualized Volatility",
    f"{volatility:.2%}"
)

col5.metric(
    "Maximum Drawdown",
    f"{max_drawdown:.2%}"
)

# AI PRICE PREDICTION

st.subheader("🤖 AI Prediction Engine")

features = [[
    latest["Open"],
    latest["High"],
    latest["Low"],
    latest["Close"],
    latest["Volume"],
    latest["MA10"],
    latest["MA20"],
    latest["Return"]
]]

prediction = model.predict(features)[0]

st.metric(
    "Predicted Next Day Price",
    f"₹{prediction:.2f}"
)

# BUY / SELL SIGNAL

current_price = latest["Close"]

if prediction > current_price:
    signal = "BUY"
    st.success(" BUY Signal")
else:
    signal = "SELL"
    st.error(" SELL Signal")

# CONFIDENCE SCORE

difference = abs(
    prediction - current_price
)

confidence = min(
    (difference / current_price)
    * 100 * 10,
    100
)

st.metric(
    "Confidence Score",
    f"{confidence:.1f}%"
)

# LIVE STOCK DATA

st.subheader(" Live Market Data")

stock = st.selectbox(
    "Select Stock",
    [
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS",
        "HDFCBANK.NS"
    ]
)

if st.button("Load Live Data"):

    live_df = yf.download(
        stock,
        start="2024-01-01",
        auto_adjust=True,
        progress=False
    )

    st.success(
        f"{stock} Loaded Successfully"
    )

    st.line_chart(
        live_df["Close"]
    )

    st.dataframe(
        live_df.tail()
    )

# STOCK COMPARISON

st.subheader(" Multi Stock Comparison")

comparison = pd.DataFrame()

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS"
]

for ticker in stocks:

    temp = yf.download(
        ticker,
        start="2024-01-01",
        auto_adjust=True,
        progress=False
    )

    comparison[ticker] = temp["Close"]

st.line_chart(comparison)

# PORTFOLIO ANALYTICS

st.subheader(" Portfolio Simulator")

investment = st.number_input(
    "Investment Amount (₹)",
    min_value=1000,
    value=100000
)

allocation = investment / len(stocks)

portfolio_value = allocation * len(stocks)

st.metric(
    "Portfolio Value",
    f"₹{portfolio_value:,.0f}"
)

# TRADE RECOMMENDATION

st.subheader(" Recommendation")

if signal == "BUY":

    st.success(
        f"""
        Recommendation:
        BUY

        Predicted Price:
        ₹{prediction:.2f}

        Current Price:
        ₹{current_price:.2f}
        """
    )

else:

    st.warning(
        f"""
        Recommendation:
        SELL

        Predicted Price:
        ₹{prediction:.2f}

        Current Price:
        ₹{current_price:.2f}
        """
    )

st.success(
    " AI Stock Trading Dashboard Loaded Successfully"
)