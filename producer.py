import json
import random
import time
from kafka import KafkaProducer
from datetime import datetime, timedelta

# Kafka settings
bootstrap_servers = ['localhost:9092']
topic_name = 'retail_sales_topic'

# Kafka producer
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Store names (example)
store_names = ['Store_A', 'Store_B', 'Store_C']

# Function to generate synthetic data
def generate_sales_data():
    order_id = random.randint(100000, 999999)
    timestamp = datetime.now() - timedelta(minutes=random.randint(0, 1440))  # Random timestamp in the last 24 hours
    store = random.choice(store_names)
    amount = round(random.uniform(10, 500), 2)  # Random amount between 10 and 500
    return {
        'order_id': order_id,
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'store': store,
        'amount': amount
    }

# Loop to generate and send data to Kafka
message_count = 0
while message_count < 1000:  # Send 1000 messages
    message = generate_sales_data()
    producer.send(topic_name, message)
    print(f"Sent message: {message}")
    message_count += 1
    time.sleep(1)  # Delay for 1 second to simulate real-time data generation

producer.close()
