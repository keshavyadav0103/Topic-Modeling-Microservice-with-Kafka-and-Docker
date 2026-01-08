import os
import json
import logging
from kafka import KafkaConsumer, KafkaProducer
from gensim import corpora, models
from gensim.utils import simple_preprocess
import nltk
from nltk.corpus import stopwords

# Set up logging
logging.basicConfig(level=logging.INFO)

# Download stopwords
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

stop_words = stopwords.words('english')

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
INPUT_TOPIC = os.environ.get('INPUT_TOPIC', 'input_text')
OUTPUT_TOPIC = os.environ.get('OUTPUT_TOPIC', 'topic_modeling_results')

# Initialize Kafka Consumer and Producer
consumer = KafkaConsumer(
    INPUT_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def preprocess(text):
    return [word for word in simple_preprocess(text) if word not in stop_words]

def train_lda(data):
    # Create a corpus from a list of texts
    dictionary = corpora.Dictionary(data)
    corpus = [dictionary.doc2bow(text) for text in data]
    # Train the LDA model
    lda = models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15)
    return lda, dictionary

def main():
    logging.info("Starting topic modeling microservice...")
    documents = []
    for message in consumer:
        text_data = message.value
        doc_id = text_data.get('id')
        text = text_data.get('text')
        logging.info(f"Received message: {doc_id}")

        if text:
            documents.append(preprocess(text))

            # For simplicity, we retrain the model with each new document.
            # In a real-world scenario, you might train on a larger batch
            # or update the model online.
            if len(documents) > 1:
                lda_model, dictionary = train_lda(documents)
                
                # Get topic distribution for the latest document
                latest_doc_bow = dictionary.doc2bow(documents[-1])
                topics = lda_model.get_document_topics(latest_doc_bow)
                
                # Prepare the output message
                output_message = {
                    'id': doc_id,
                    'topics': [(topic_id, str(prob)) for topic_id, prob in topics]
                }
                
                # Send the results to the output topic
                producer.send(OUTPUT_TOPIC, output_message)
                producer.flush()
                logging.info(f"Processed and sent topics for document: {doc_id}")

if __name__ == "__main__":
    main()
