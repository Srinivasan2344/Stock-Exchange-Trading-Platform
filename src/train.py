import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

# Load processed data
df = pd.read_csv("data/processed_stock_data.csv")

# Features
features = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
    "MA10",
    "MA20",
    "Return"
]

X = df[features]
y = df["Target"]

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    shuffle=False
)

# Model
model = XGBRegressor(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Evaluate
mae = mean_absolute_error(y_test, predictions)

print(f"MAE: {mae:.2f}")

# Save model
joblib.dump(model, "models/xgboost_model.pkl")

print("Model saved successfully")