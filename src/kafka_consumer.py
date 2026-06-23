from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "stock_prices",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m:
    json.loads(m.decode("utf-8"))
)

print("Waiting for Messages...")

for message in consumer:

    print(
        message.value
    )