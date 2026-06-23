
from fastapi import FastAPI
import pandas as pd
import joblib
from sqlalchemy import create_engine
from fraud_detection import detect_fraud
from news_sentiment import ( analyze_stock_news )


app = FastAPI(
    title="AI Stock Trading API",
    version="1.0"
)

# -----------------------------
# DATABASE
# -----------------------------

engine = create_engine(
    "postgresql://postgres:durai123@localhost:5432/stock_trading"
)

# -----------------------------
# LOAD MODEL & DATA
# -----------------------------

df = pd.read_csv(
    "data/processed_stock_data.csv"
)

model = joblib.load(
    "models/xgboost_model.pkl"
)

# -----------------------------
# HOME
# -----------------------------

@app.get("/")
def home():

    return {
        "message": "AI Stock Trading API Running"
    }

# -----------------------------
# AI PREDICTION
# -----------------------------

@app.get("/predict")
def predict():

    latest = df.iloc[-1]

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

    return {
        "current_price": float(
            latest["Close"]
        ),
        "predicted_price": float(
            prediction
        )
    }

# -----------------------------
# BUY / SELL SIGNAL
# -----------------------------

@app.get("/signal")
def signal():

    latest = df.iloc[-1]

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

    current_price = latest["Close"]

    if prediction > current_price:
        result = "BUY"
    else:
        result = "SELL"

    return {
        "signal": result,
        "current_price": float(
            current_price
        ),
        "predicted_price": float(
            prediction
        )
    }

# -----------------------------
# RISK ANALYTICS
# -----------------------------

@app.get("/risk")
def risk():

    returns = df["Return"]

    volatility = (
        returns.std()
        * (252 ** 0.5)
    )

    cumulative = (
        1 + returns
    ).cumprod()

    running_max = (
        cumulative.cummax()
    )

    drawdown = (
        cumulative - running_max
    ) / running_max

    max_drawdown = drawdown.min()

    return {
        "annualized_volatility":
        float(volatility),

        "maximum_drawdown":
        float(max_drawdown)
    }

# -----------------------------
# PORTFOLIO
# -----------------------------

@app.get("/portfolio")
def get_portfolio():

    portfolio_df = pd.read_sql(
        "SELECT * FROM portfolio",
        engine
    )

    return portfolio_df.to_dict(
        orient="records"
    )

# -----------------------------
# TRADE HISTORY
# -----------------------------

@app.get("/trade-history")
def trade_history():

    trade_df = pd.read_sql(
        "SELECT * FROM trade_history",
        engine
    )

    return trade_df.to_dict(
        orient="records"
    )

# -----------------------------
# PORTFOLIO SUMMARY
# -----------------------------

@app.get("/portfolio-summary")
def portfolio_summary():

    portfolio_df = pd.read_sql(
        "SELECT * FROM portfolio",
        engine
    )

    if portfolio_df.empty:

        return {
            "message":
            "No Portfolio Data"
        }

    portfolio_df["investment"] = (
        portfolio_df["quantity"]
        * portfolio_df["buy_price"]
    )

    total_value = (
        portfolio_df["investment"]
        .sum()
    )

    return {
        "total_portfolio_value":
        float(total_value),

        "total_holdings":
        int(
            len(portfolio_df)
        )
    }

# -----------------------------
# MARKET ALERT
# -----------------------------

@app.get("/market-alert")
def market_alert():

    latest = df.iloc[-1]

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

    current_price = latest["Close"]

    if prediction > current_price * 1.02:

        alert = "Strong BUY"

    elif prediction < current_price * 0.98:

        alert = "Strong SELL"

    else:

        alert = "HOLD"

    return {
        "alert": alert,
        "current_price":
        float(current_price),
        "predicted_price":
        float(prediction)
    }

# -----------------------------
# HEALTH CHECK


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

@app.get("/fraud-detection")
def fraud_detection():

    trades = [
        {"quantity": 10, "price": 1500},
        {"quantity": 15, "price": 1800},
        {"quantity": 12, "price": 1700},
        {"quantity": 5000, "price": 50000}
    ]

    return detect_fraud(trades)

@app.get("/news-sentiment")
def news_sentiment():

    return analyze_stock_news(
        "Reliance Industries"
    )
