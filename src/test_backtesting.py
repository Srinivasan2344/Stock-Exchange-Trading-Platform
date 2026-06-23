from backtesting import evaluate_predictions

actual = [100, 105, 110, 120]

predicted = [102, 103, 111, 118]

print(
    evaluate_predictions(
        actual,
        predicted
    )
)