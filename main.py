from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def scrapper():
    sources = ['https://www.dawn.com/', 'https://www.bbc.com/']
    all_data = []
    for source in sources:
        response = requests.get(source)
        soup = BeautifulSoup(response.text, 'html.parser')
        tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        data = [(tag.name, tag.get_text(strip=True)) for tag in tags]
        all_data.extend(data)
    return all_data

def data_transformation(ti):
    extracted_data = ti.xcom_pull(task_ids='extract_data')
    df = pd.DataFrame(extracted_data, columns=['Tag', 'Content'])
    df['Content'] = df['Content'].str.replace(r'\n|\r', ' ', regex=True).str.strip()
    df.to_csv('transformed_data.csv', index=False)

def store_data():
    pass

with DAG(
    'data_extraction_pipeline',
    default_args=default_args,
    description='DAG for extracting, transforming, and storing data',
    schedule_interval=timedelta(days=1),
) as dag:

    extract_data = PythonOperator(
        task_id='extract_data',
        python_callable=scrapper,
    )

    transform_data = PythonOperator(
        task_id='transform_data',
        python_callable=data_transformation,
    )

    store_data_task = PythonOperator(
        task_id='store_data',
        python_callable=store_data,
    )

    extract_data >> transform_data >> store_data_task
