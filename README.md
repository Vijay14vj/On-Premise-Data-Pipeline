# 🌦️ Full-Stack On-Premise Data Pipeline for IoT & Weather Data

## 📌 Project Overview

This project simulates a real-time data engineering pipeline for a hypothetical weather analytics company. The system is designed to ingest, process, transform, and store IoT sensor and real-time weather data using a full suite of big data and orchestration tools.

---

## 🎯 Objectives

- Ingest real-time data from the **OpenWeatherMap API** into Kafka
- Simulate IoT data using **Faker** and store it as CSV and in **MySQL**
- Use **Apache Spark** for both **Streaming (Kafka → Parquet)** and **Batch ETL (CSV + MySQL → Hive, MySQL)**
- Orchestrate workflows using **Apache Airflow**
- Monitor the pipeline using **Grafana** and **Prometheus**
- (Optional) Containerize the full pipeline using **Docker Compose**

---

## 🧰 Tech Stack

| Technology       | Purpose                            |
|------------------|-------------------------------------|
| **Python**       | Scripting and orchestration         |
| **Kafka**        | Real-time streaming ingestion       |
| **Spark**        | Streaming and batch processing      |
| **Hive**         | Data lake table for processed data  |
| **MySQL**        | Historical and final storage        |
| **Airflow**      | Workflow orchestration              |
| **Grafana + Prometheus** | Monitoring pipeline health     |
| **Docker Compose (Optional)** | Container orchestration     |

---

## 🧪 Project Components

### 1. Ingestion

#### 🌀 Weather API to Kafka
- Pulls real-time weather data from **OpenWeatherMap API**
- Publishes to Kafka topic `weather-topic`
- Scheduled using Airflow DAG `weather_to_kafka_dag.py`

#### 🤖 Faker to CSV
- Generates fake IoT weather logs using `Faker` (e.g., name, city, temperature)
- Saves data as `weather_logs.csv` every minute

#### 🛢️ MySQL Mock Data
- Inserts fake device/sensor records into MySQL table via Python script

---

### 2. Processing

#### 🔁 Spark Streaming
- Reads data from Kafka topic `weather-topic`
- Saves as Parquet files every 5 minutes using `streaming_kafka_to_parquet.py`

#### 🧪 Spark Batch ETL
- Reads CSV and MySQL data
- Performs transformation (e.g., joins, filters)
- Loads final result into:
  - Hive Table: `final_table`
  - MySQL Table: `final_table`
- Handled by `batch_etl.py`

---

### 3. Storage & Output

- Parquet files: `/weather/parquet_data/`
- Hive table: `default.final_table`
- MySQL: `weather.final_table`

---

### 4. Orchestration & Monitoring

- **Airflow DAGs**:
  - `weather_to_kafka_dag.py`
  - `batch_etl_dag.py`

- **Grafana Dashboard** (optional):
  - Monitors Airflow DAGs, Spark jobs, and Docker containers
  - Exported JSON file included (if implemented)

---

## 📁 Folder Structure

onprem-data-pipeline-yourname/
├── airflow/
│ ├── dags/
│ │ ├── weather_to_kafka_dag.py
│ │ └── batch_etl_dag.py
├── kafka/
│ └── weather_producer.py
├── spark/
│ ├── streaming_kafka_to_parquet.py
│ └── batch_etl.py
├── faker/
│ ├── generate_csv.py
│ └── load_mysql.py
├── hive/
│ └── create_final_table.sql
├── docker/
│ └── docker-compose.yml (optional)
├── grafana/
│ └── dashboard.json (optional)
└── README.md


## Author

Vijay M
