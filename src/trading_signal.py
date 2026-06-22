import pandas as pd
df = pd.read_csv("data/processed_stock_data.csv")

latest = df.iloc[-1]

score = 0

# Moving Average
if latest["MA10"] > latest["MA20"]:
    score += 1
else:
    score -= 1

# RSI
if latest["RSI"] < 30:
    score += 1
elif latest["RSI"] > 70:
    score -= 1

# MACD
if latest["MACD"] > latest["Signal_Line"]:
    score += 1
else:
    score -= 1

sentiment_score = 0.5

if sentiment_score > 0:
    score += 1
else:
    score -= 1

if score >= 2:
    signal = "STRONG BUY"
elif score == 1:
    signal = "BUY"
elif score == 0:
    signal = "HOLD"
elif score == -1:
    signal = "SELL"
else:
    signal = "STRONG SELL"

print("Trading Signal:", signal)
print("Score:", score)
confidence = ((score + 4) / 8) * 100
print("Confidence:", round(confidence, 2), "%")