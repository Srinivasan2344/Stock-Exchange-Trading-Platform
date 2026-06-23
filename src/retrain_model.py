import pandas as pd
import joblib

from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Load latest data

df = pd.read_csv(
    "data/processed_stock_data.csv"
)

# Features

X = df[
    [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "MA10",
        "MA20",
        "Return"
    ]
]

# Target

y = df["Close"].shift(-1)

# Remove last row

X = X[:-1]
y = y[:-1]

# Split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train

model = XGBRegressor()

model.fit(
    X_train,
    y_train
)

# Evaluate

predictions = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    predictions
)

print("Model Retrained")
print("MAE:", mae)

# Save new model

joblib.dump(
    model,
    "models/xgboost_model.pkl"
)

print("New Model Saved")