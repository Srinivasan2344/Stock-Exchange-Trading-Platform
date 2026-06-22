from fastapi import FastAPI
import pandas as pd
import joblib

app = FastAPI()

model = joblib.load("models/xgboost_model.pkl")

@app.get("/")
def home():
    return {"message": "Stock Prediction API Running"}

@app.get("/predict")
def predict():

    df = pd.read_csv(
        "data/processed_stock_data.csv"
    )

    latest = df.iloc[-1]

    features = pd.DataFrame([{
        "Open": latest["Open"],
        "High": latest["High"],
        "Low": latest["Low"],
        "Close": latest["Close"],
        "Volume": latest["Volume"],
        "MA10": latest["MA10"],
        "MA20": latest["MA20"],
        "Return": latest["Return"]
    }])

    prediction = model.predict(features)

    return {
        "predicted_price": float(prediction[0])
    }

@app.get("/signal")
def signal():

    df = pd.read_csv(
        "data/processed_stock_data.csv"
    )

    latest = df.iloc[-1]

    if latest["MA10"] > latest["MA20"]:
        signal = "BUY"
    elif latest["MA10"] < latest["MA20"]:
        signal = "SELL"
    else:
        signal = "HOLD"

    return {
        "signal": signal
    }