# 🛍️ Real-Time Retail Sales Data Pipeline using Kafka and BigQuery

This project implements a real-time data pipeline that simulates retail sales transactions using **Apache Kafka** and stores them in **Google BigQuery** for analysis. It’s designed to mimic a simple ETL (Extract, Transform, Load) pipeline built on a local environment and integrated with cloud storage.

---

## 🚀 Features

- **Simulated Retail Data Stream**: Generates random sales transactions with fields: `order_id`, `timestamp`, `store`, and `amount`.
- **Apache Kafka Integration**: Kafka producer sends data to a topic; consumer reads and processes the messages.
- **Google BigQuery Integration**: Batches the received data and uploads it periodically using service account authentication.
- **Local Development Ready**: Fully configured to run in a local environment (no cloud deployment needed).
- **Secure by Default**: Service account key is excluded using `.gitignore`.

---

## 🧱 Tech Stack

- 🐍 Python
- 🔄 Apache Kafka
- ☁️ Google BigQuery
- 🧪 Google Cloud SDK
- 🛡️ Service Account Authentication

---

## 📦 Project Structure

```
retail-sales-data-pipeline/
│
├── src/
│   ├── producer.py           # Kafka producer that sends simulated data
│   ├── consumer.py           # Kafka consumer that writes to BigQuery
│
├── requirements.txt          # Python dependencies
├── .gitignore                # Excludes sensitive files
├── README.md                 # This file
```

---

## ⚙️ How to Run

### 1. ✅ Prerequisites

- Python 3.8+
- Apache Kafka (local setup)
- Google Cloud account with BigQuery enabled
- Service account key JSON (keep it private!)

### 2. 📥 Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. 🛠️ Configure Kafka

Make sure your Kafka server is running locally (default: `localhost:9092`).  
Create a Kafka topic:

```bash
kafka-topics.sh --create --topic retail_sales --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### 4. 🔑 Set Up Google BigQuery Credentials

Save your service account key (e.g., `your-key.json`) and replace the path in `consumer.py`:

```python
service_account.Credentials.from_service_account_file("path/to/your-key.json")
```

### 5. 🗂️ BigQuery Setup

Make sure this exists in your BigQuery:
- **Project ID**: `retail-sales-pipeline-455810`
- **Dataset Name**: `retail_dataset`
- **Table Name**: `retail_sales`
- With the schema:
  - `order_id` (STRING)
  - `timestamp` (STRING)
  - `store` (STRING)
  - `amount` (FLOAT)

_Note: Free-tier BigQuery does not support streaming inserts. So this pipeline writes in batch intervals._

### 6. 🚦 Run the Pipeline

In separate terminals:

**Producer:**

```bash
python src/producer.py
```

**Consumer:**

```bash
python src/consumer.py
```

---

## 📊 BigQuery Schema

| Field      | Type    |
|------------|---------|
| order_id   | STRING  |
| timestamp  | STRING  |
| store      | STRING  |
| amount     | FLOAT   |

---

## 🛡️ Security Note

This repo uses `.gitignore` to exclude:
- Service account key files
- Any sensitive credentials

**Never commit your service key JSON to GitHub.** If you did it accidentally:
1. Remove it from history:  
   ```bash
   git rm --cached 'security key.json'
   git commit --amend --no-edit
   git push --force
   ```
2. Revoke and regenerate your key from the [Google Cloud Console](https://console.cloud.google.com/iam-admin/serviceaccounts).

---

## 🧠 Learning Outcome

- Kafka real-time message flow
- Integration of cloud services with local development
- Understanding how to batch insert to BigQuery from Python
- Managing credentials securely in GitHub

---

## 📘 License

This project is for educational and demo purposes. Feel free to fork, explore, and extend!

---

## ✨ Author

**Premnadh Gajula**  
Computer Science & Engineering (AIML), SRMAP University