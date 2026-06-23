
import streamlit as st
import pandas as pd
import yfinance as yf
import joblib
from sqlalchemy import create_engine
from src.portfolio_recommendation import recommend_portfolio
from src.market_alert import generate_alert

st.set_page_config(
    page_title="AI Stock Trading Dashboard",
    layout="wide"
)

st.title("AI Stock Trading Dashboard")

# LOAD DATA


df = pd.read_csv("data/processed_stock_data.csv")
model = joblib.load("models/xgboost_model.pkl")

latest = df.iloc[-1]
# LATEST METRICS

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


# STOCK PRICE TREND


st.subheader("Stock Price Trend")

st.line_chart(
    df.set_index("Date")["Close"]
)


# MOVING AVERAGES


st.subheader("Moving Averages")

st.line_chart(
    df.set_index("Date")[["Close", "MA10", "MA20"]]
)


# RECENT DATA


st.subheader("Recent Data")
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

st.subheader("Risk Metrics")

col4, col5 = st.columns(2)

col4.metric(
    "Annualized Volatility",
    f"{volatility:.2%}"
)

col5.metric(
    "Maximum Drawdown",
    f"{max_drawdown:.2%}"
)

# AI PREDICTION

st.subheader(" AI Prediction Engine")

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

current_price = latest["Close"]

if prediction > current_price:
    signal = "BUY"
    st.success(" BUY Signal")
else:
    signal = "SELL"
    st.error(" SELL Signal")

difference = abs(
    prediction - current_price
)

confidence = min(
    (difference / current_price) * 100 * 10,
    100
)

st.metric(
    "Confidence Score",
    f"{confidence:.1f}%"
)


# LIVE MARKET DATA

st.subheader("Live Market Data")

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

# PORTFOLIO

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

    if not portfolio_df.empty:

        portfolio_df["investment"] = (
            portfolio_df["quantity"]
            * portfolio_df["buy_price"]
        )

        total_value = portfolio_df[
            "investment"
        ].sum()

        st.subheader(" Portfolio Summary")

        c1, c2 = st.columns(2)

        c1.metric(
            "Total Portfolio Value",
            f"₹{total_value:,.2f}"
        )

        c2.metric(
            "Total Holdings",
            len(portfolio_df)
        )

        portfolio_list = portfolio_df[
            ["stock", "quantity", "buy_price"]
        ].to_dict("records")

        recommendations = recommend_portfolio(
            portfolio_list
        )

        st.subheader(
            " Portfolio Recommendations"
        )

        for rec in recommendations:
            st.warning(rec)

except Exception as e:

    st.warning(
        f"Portfolio Error: {e}"
    )

# TRADE HISTORY

st.subheader(" Trade History")

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

# PORTFOLIO SIMULATOR

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

# FINAL RECOMMENDATION

st.subheader(" Trading Recommendation")

if signal == "BUY":

    st.success(
        f"""
Recommendation: BUY

Predicted Price: ₹{prediction:.2f}

Current Price: ₹{current_price:.2f}
"""
    )

else:

    st.warning(
        f"""
Recommendation: SELL

Predicted Price: ₹{prediction:.2f}

Current Price: ₹{current_price:.2f}
"""
    )

st.success(
    " AI Stock Trading Dashboard Loaded Successfully"
)

alert = generate_alert(
    current_price,
    prediction
)

st.subheader(" Market Alert")

st.info(alert)