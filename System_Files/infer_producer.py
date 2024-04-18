from confluent_kafka import Producer
from kafka_broker import kafka_broker, kafka_topic

producer = Producer({'bootstrap.servers': kafka_broker})

for i in range(20):
    producer.produce(kafka_topic,f"{i}".encode('utf-8'))

producer.flush()