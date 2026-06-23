import pandas as pd
from trading_signal import generate_signal

df = pd.read_csv("data/processed_stock_data.csv")

signal, confidence = generate_signal(df)

print("Signal:", signal)
print("Confidence:", confidence, "%")