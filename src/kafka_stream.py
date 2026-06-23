from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v:
    json.dumps(v).encode("utf-8")
)

data = {
    "stock": "RELIANCE.NS",
    "price": 1500
}

producer.send(
    "stock_prices",
    data
)

producer.flush()

print("Message Sent")