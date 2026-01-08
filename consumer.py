import json
from kafka import KafkaConsumer


KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
OUTPUT_TOPIC = 'topic_modeling_results'


consumer = KafkaConsumer(
    OUTPUT_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

def main():
    print("Listening for topic modeling results...")
    for message in consumer:
        result = message.value
        print(f"Received result: {result}")

if __name__ == "__main__":
    main()
