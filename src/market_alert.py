def generate_alert(
    current_price,
    predicted_price
):

    if predicted_price > current_price * 1.02:
        return "🚀 Strong BUY Alert"

    elif predicted_price < current_price * 0.98:
        return "⚠ Strong SELL Alert"

    return " HOLD"