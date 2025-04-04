import json
import time
from kafka import KafkaConsumer
from google.cloud import bigquery
from google.oauth2 import service_account
from collections import deque

# Kafka consumer setup
consumer = KafkaConsumer(
    'retail_sales_data',  # Kafka topic
    bootstrap_servers=['localhost:9092'],  # Kafka broker
    group_id='retail_sales_group',  # Consumer group
    auto_offset_reset='earliest',  # Start from the earliest message if no offset exists
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))  # Deserialize JSON messages
)

# BigQuery client setup
# Replace with your service account JSON key
credentials = service_account.Credentials.from_service_account_file(
    'enter you security key file'
)

client = bigquery.Client(credentials=credentials, project=credentials.project_id)
dataset_id = 'retail_dataset'
table_id = 'retail_sales'

# Function to insert data into BigQuery
def insert_into_bigquery(data):
    try:
        # Prepare the data to be inserted into BigQuery
        rows_to_insert = [
            {
                "order_id": record['order_id'],
                "timestamp": record['timestamp'],
                "store": record['store'],
                "amount": record['amount']
            }
            for record in data
        ]
        
        # Insert data into BigQuery table
        errors = client.insert_rows_json(f"{dataset_id}.{table_id}", rows_to_insert)
        
        if errors == []:
            print(f"Successfully inserted {len(data)} records into BigQuery")
        else:
            print(f"Error inserting data: {errors}")
    except Exception as e:
        print(f"Error: {e}")

# Batching parameters
batch_size = 100  # Number of messages to accumulate before inserting into BigQuery
flush_interval = 10  # Interval (in seconds) to flush the buffer

# Queue to hold accumulated messages
message_buffer = deque()

# Consume messages and accumulate them into batches
try:
    print("Starting consumer...")
    start_time = time.time()
    
    for message in consumer:
        # Add the message to the buffer
        message_buffer.append(message.value)
        
        # If the buffer reaches the batch size or the flush interval has passed, insert into BigQuery
        if len(message_buffer) >= batch_size or (time.time() - start_time) >= flush_interval:
            print(f"Flushing {len(message_buffer)} records to BigQuery...")
            insert_into_bigquery(list(message_buffer))  # Insert the batch into BigQuery
            message_buffer.clear()  # Clear the buffer after inserting
            start_time = time.time()  # Reset the timer after flushing

except KeyboardInterrupt:
    print("Consumer stopped.")
finally:
    consumer.close()
