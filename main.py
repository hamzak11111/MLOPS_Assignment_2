from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os

default_args = {
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
    csv_file = 'transformed_data.csv'
    dvc_repo_dir = 'dvc_folder'
    dvc_data_dir = os.path.join(dvc_repo_dir, 'data')
    os.makedirs(dvc_data_dir, exist_ok=True)
    dvc_file_path = os.path.join(dvc_data_dir, csv_file)
    os.rename(csv_file, dvc_file_path)
    os.chdir(dvc_repo_dir)
    os.system('dvc add ' + dvc_file_path)
    os.system('dvc commit')
    os.system('dvc push')
    os.system('git add .')
    os.system('git commit -m "changes committed"')
    os.system('git push origin main')

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
