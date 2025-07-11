from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from scripts.weather_api_producer import fetch_weather_data
from scripts.faker_csv_generator import generate_fake_csv
from scripts.mysql_data_loader import load_mock_data_to_mysql

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'weather_to_kafka_dag',
    default_args=default_args,
    description='DAG to fetch weather data and send to Kafka',
    schedule_interval='* * * * *',
    catchup=False
)

fetch_weather_task = PythonOperator(
    task_id='fetch_weather_data',
    python_callable=fetch_weather_data,
    dag=dag
)

generate_csv_task = PythonOperator(
    task_id='generate_fake_csv',
    python_callable=generate_fake_csv,
    dag=dag
)

load_mysql_task = PythonOperator(
    task_id='load_mock_data_to_mysql',
    python_callable=load_mock_data_to_mysql,
    dag=dag
)

fetch_weather_task >> [generate_csv_task, load_mysql_task]