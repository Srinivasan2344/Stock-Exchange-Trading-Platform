from sklearn.metrics import mean_absolute_error

def evaluate_predictions(actual, predicted):

    mae = mean_absolute_error(actual, predicted)

    accuracy = (
        1 - (mae / (sum(actual) / len(actual)))
    ) * 100

    return {
        "MAE": round(mae, 2),
        "Accuracy": round(accuracy, 2)
    }