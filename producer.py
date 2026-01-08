import json
from kafka import KafkaProducer
import time


KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
INPUT_TOPIC = 'input_text'


producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


documents = [
    {"id": 1, "text": "The quick brown fox jumps over the lazy dog."},
    {"id": 2, "text": "Never jump over the lazy dog quickly."},
    {"id": 3, "text": "The five boxing wizards jump quickly."},
    {"id": 4, "text": "Pack my box with five dozen liquor jugs."},
    {"id": 5, "text": "The job of a software engineer is to build and maintain software systems."},
    {"id": 6, "text": "Data science is an inter-disciplinary field that uses scientific methods, processes, algorithms and systems to extract knowledge and insights from structured and unstructured data."},
    {"id": 7, "text": "Machine learning is a field of inquiry devoted to understanding and building methods that 'learn' – that is, methods that leverage data to improve performance on some set of tasks."},
    {"id": 8, "text": "The field of data science and machine learning are closely related."},
    {"id": 9, "text": "The stock market is a complex system of buying and selling shares of publicly traded companies."},
    {"id": 10, "text": "Investors can make a lot of money in the stock market, but they can also lose a lot of money."}
]

def main():
    for doc in documents:
        producer.send(INPUT_TOPIC, doc)
        print(f"Sent document: {doc['id']}")
        time.sleep(2)
    producer.flush()

if __name__ == "__main__":
    main()
