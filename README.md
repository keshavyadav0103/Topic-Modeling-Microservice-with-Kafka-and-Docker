# Topic Modeling Microservice with Kafka and Docker

This project demonstrates a **Kafka-based microservice architecture** for performing **topic modeling on text data** using **Latent Dirichlet Allocation (LDA)**.  
The system consumes text messages from a Kafka topic, applies topic modeling, and publishes the results to another Kafka topic.  
All components are containerized using **Docker** and orchestrated with **Docker Compose**.

---

## Architecture Overview

- **Producer** → Sends raw text documents to Kafka
- **Kafka (Zookeeper + Broker)** → Message streaming backbone
- **Topic Modeling Microservice**
  - Consumes text from Kafka
  - Applies preprocessing and LDA topic modeling
  - Publishes topic distributions to an output topic
- **Consumer** → Reads and displays topic modeling results

---

## Technologies Used

- Python  
- Apache Kafka  
- Zookeeper  
- Gensim (LDA)  
- Docker  
- Docker Compose  

---

## Prerequisites

Ensure the following are installed on your system:

- Docker  
- Docker Compose  
- Python 3.8+ (for running producer and consumer scripts locally)




## Running the Project

1.  **Start the services:**

    Open a terminal in the root of the project and run:

    ```bash
    docker-compose up -d --build
    ```

    This will start Zookeeper, Kafka, and the topic modeling microservice.

2.  **Send data to the input topic:**

    Open another terminal and run the producer script:

    ```bash
    python producer.py
    ```

    This will send sample text documents to the `input_text` Kafka topic.

3.  **View the results:**

    Open a third terminal and run the consumer script:

    ```bash
    python consumer.py
    ```

    This will consume the topic modeling results from the `topic_modeling_results` Kafka topic and print them to the console.

4.  **Stopping the services:**

    To stop the services, run:

    ```bash
    docker-compose down
    ```
