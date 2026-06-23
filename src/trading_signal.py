import pandas as pd


def calculate_rsi(data, period=14):
    delta = data["Close"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_macd(data):
    ema12 = data["Close"].ewm(span=12, adjust=False).mean()
    ema26 = data["Close"].ewm(span=26, adjust=False).mean()

    macd = ema12 - ema26
    signal_line = macd.ewm(span=9, adjust=False).mean()

    return macd, signal_line


def generate_signal(df):

    df = df.copy()

    # RSI
    df["RSI"] = calculate_rsi(df)

    # MACD
    df["MACD"], df["Signal_Line"] = calculate_macd(df)

    latest = df.iloc[-1]

    ma10 = latest["MA10"]
    ma20 = latest["MA20"]
    rsi = latest["RSI"]
    macd = latest["MACD"]
    signal_line = latest["Signal_Line"]

    buy_conditions = 0
    sell_conditions = 0

    # Moving Average Signal
    if ma10 > ma20:
        buy_conditions += 1
    else:
        sell_conditions += 1

    # RSI Signal
    if rsi < 30:
        buy_conditions += 1
    elif rsi > 70:
        sell_conditions += 1

    # MACD Signal
    if macd > signal_line:
        buy_conditions += 1
    else:
        sell_conditions += 1

    # Final Decision
    if buy_conditions >= 2:
        signal = "BUY"
    elif sell_conditions >= 2:
        signal = "SELL"
    else:
        signal = "HOLD"

    confidence = round(
        max(buy_conditions, sell_conditions) / 3 * 100,
        2
    )

    return signal, confidence