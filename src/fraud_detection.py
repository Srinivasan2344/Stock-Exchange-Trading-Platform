import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_fraud(trades):

    df = pd.DataFrame(trades)

    model = IsolationForest(
        contamination=0.1,
        random_state=42
    )

    df["anomaly"] = model.fit_predict(
        df[["quantity", "price"]]
    )

    frauds = df[
        df["anomaly"] == -1
    ]

    return frauds.to_dict(
        orient="records"
    )