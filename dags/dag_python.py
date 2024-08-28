from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from datetime import datetime, timedelta
import pendulum
from google.cloud import storage, bigquery
# from kaggle import KaggleApi
import os
import pandas as pd

default_args = {
    'owner': 'phuclee',
    'start_date': pendulum.datetime(2024, 8, 19, tz="Asia/Ho_Chi_Minh"),
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'data_pipeline_v1',
    default_args=default_args,
    description='Daily data pipeline',
    schedule_interval='0 7 * * *',
    catchup=False,
)

# Download data from kaggle need Kaggle.json
# def download_dataset(**kwargs):
#     dataset_name = 'pushshift/tu_erichartleyfrnd'
#     output_path = 'data/'

#     api = KaggleApi()
#     api.authenticate()

#     os.makedirs(output_path, exist_ok=True)

#     api.dataset_download_files(dataset_name, path=output_path, unzip=True)


def convert_and_compress_data():

    input_file = '/opt/airflow/data/data.ndjson'
    output_file = '/opt/airflow/data/data.csv.gz'

    df = pd.read_json(input_file, lines=True)
    df.to_csv(output_file, index=False,  compression='gzip')


def upload_to_gcs():

    client = storage.Client.from_service_account_json(
        json_credentials_path='credentials-python-storage.json')
    bucket_name = 'nexar-test'
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob('data.csv.gz')
    blob.upload_from_filename('data/data.csv.gz')


def load_csv_from_gcs_to_bigquery():

    dataset_id = "skilful-answer-432616-m6.nexar_test"
    table_id = "twitter-comment"
    gcs_uri = "gs://nexar-test/data.csv.gz"

    client = bigquery.Client.from_service_account_json(
        json_credentials_path='credentials-python-storage.json')

    table_ref = client.dataset(dataset_id).table(table_id)

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
    )

    load_job = client.load_table_from_uri(
        gcs_uri,
        table_ref,
        job_config=job_config,
    )

    load_job.result()

def load_csv_from_local_to_bigquery():

    dataset_id = "skilful-answer-432616-m6.nexar_test"
    table_id = "twitter"

    client = bigquery.Client.from_service_account_json(
        json_credentials_path='/opt/airflow/credentials-python-storage.json')

    table_ref = client.dataset(dataset_id).table(table_id)

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
    )

    with open("/opt/airflow/data/data.csv.gz", "rb") as source_file:
        load_job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

    load_job.result()


convert_compress_task = PythonOperator(
    task_id='convert_task',
    python_callable=convert_and_compress_data,
    dag=dag
)

# load_to_bq_task = PythonOperator(
#     task_id="load_to_bq",
#     python_callable=load_csv_from_local_to_bigquery,
#     dag=dag
# )
convert_compress_task
