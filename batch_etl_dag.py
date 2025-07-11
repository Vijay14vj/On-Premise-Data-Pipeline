from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

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
    'batch_etl_dag',
    default_args=default_args,
    description='DAG to run Spark batch ETL job',
    schedule_interval='*/5 * * * *',
    catchup=False
)

spark_etl_task = BashOperator(
    task_id='run_spark_etl',
    bash_command='spark-submit --master spark://spark:7077 /app/batch_etl.py',
    dag=dag
)

spark_etl_task