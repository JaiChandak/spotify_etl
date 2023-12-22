from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from spotify_etl import run_spotify_etl

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 12, 22),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'spotify_dag',
    default_args=default_args,
    description='Basic DAG applying ETL on Spotify API',
    schedule_interval=timedelta(days=1),
)

run_etl = PythonOperator(
    task_id='complete_spotify_etl',
    python_callable=run_spotify_etl,
    dag=dag, 
)

run_etl