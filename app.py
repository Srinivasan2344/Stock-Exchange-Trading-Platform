from fastapi import FastAPI
import pandas as pd
import joblib
from src.trading_signal import generate_signal

app = FastAPI()


app = FastAPI(
    title="AI Stock Trading API"
)

model = joblib.load(
    "models/xgboost_model.pkl"
)

df = pd.read_csv(
    "data/processed_stock_data.csv"
)

@app.get("/")
def home():
    return {
        "message": "AI Stock Trading API Running"
    }

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

    prediction = model.predict(
        features
    )[0]

    return {
        "current_price":
            float(latest["Close"]),
        "predicted_price":
            float(prediction)
    }

@app.get("/risk")
def risk():

    returns = df["Return"]

    volatility = (
        returns.std()
        * (252 ** 0.5)
    )

    return {
        "annualized_volatility":
            float(volatility)
    }

@app.get("/sentiment")
def sentiment():

    return {
        "sentiment":
            "Positive",
        "score":
            0.22
    }

@app.get("/")
def home():
    return {"message": "Stock Trading AI API Running"}


@app.get("/signal")
def get_signal():

    df = pd.read_csv(
        "data/processed_stock_data.csv"
    )

    signal, confidence = generate_signal(df)

    return {
        "signal": signal,
        "confidence": confidence
    }

model = joblib.load(
    "models/xgboost_model.pkl"
)

@app.get("/predict")
def predict():

    df = pd.read_csv(
        "data/processed_stock_data.csv"
    )

    latest = df[["MA10", "MA20"]].iloc[-1:]

    prediction = model.predict(latest)

    return {
        "predicted_price": float(
            prediction[0]
        )
    }