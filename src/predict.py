import pandas as pd
import joblib

model = joblib.load("models/xgboost_model.pkl")

df = pd.read_csv("data/processed_stock_data.csv")

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

print(f"Predicted Next Day Price: {prediction[0]:.2f}")