from fraud_detection import detect_fraud

trades = [
    {"quantity": 10, "price": 1500},
    {"quantity": 15, "price": 1800},
    {"quantity": 12, "price": 1700},
    {"quantity": 5000, "price": 50000}
]

frauds = detect_fraud(trades)

print(frauds)