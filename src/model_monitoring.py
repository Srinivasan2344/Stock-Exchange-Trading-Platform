import pandas as pd

actual_price = 1200
predicted_price = 1196

threshold = 20

error = abs(
    actual_price -
    predicted_price
)

if error > threshold:
    retrain_required = True
else:
    retrain_required = False

print("Prediction Error:", error)
print("Retrain Required:", retrain_required)