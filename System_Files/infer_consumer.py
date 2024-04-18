from confluent_kafka import Consumer
from kafka_broker import kafka_broker, kafka_topic

consumer = Consumer({
    'bootstrap.servers': kafka_broker,
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe([kafka_topic])

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f'Consumer error: {msg.error()}')
        continue
    print(f'Received message: {msg.value().decode("utf-8")}')

    import requests
    import json

    reqUrl = "http://127.0.0.1:2000/predict"

    headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)",
    "Content-Type": "application/json" 
    }

    payload = json.dumps({
    "input":6
    })

    response = requests.request("POST", reqUrl, data=payload,  headers=headersList)

    print(response.text)