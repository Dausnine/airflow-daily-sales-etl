from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import pandas as pd
import os

# The path INSIDE the container (we will map this in Docker)
ONEDRIVE_PATH = '/opt/airflow/onedrive_bucket/transformed_sales.csv'

def etl_postgres_to_onedrive():
    # 1. EXTRACT: Pull from Postgres using the connection ID you created ('postgres')
    pg_hook = PostgresHook(postgres_conn_id='postgres')
    df = pg_hook.get_pandas_df(sql="SELECT * FROM raw_daily_sales;")
    
    if df.empty:
        print("No data found in Postgres.")
        return

    # 2. TRANSFORM: Cleaning and Revenue Calculation
    df['quantity'] = df['quantity'].fillna(0)
    df = df.dropna(subset=['unit_price'])
    df['total_revenue'] = df['quantity'] * df['unit_price']
    
    # 3. LOAD: Save directly to the mounted OneDrive folder
    # Create directory if it doesn't exist inside container
    os.makedirs(os.path.dirname(ONEDRIVE_PATH), exist_ok=True)
    
    df.to_csv(ONEDRIVE_PATH, index=False)
    print(f"File successfully saved to {ONEDRIVE_PATH}")

with DAG(
    dag_id='postgres_to_onedrive_etl',
    start_date=datetime(2026, 2, 12),
    schedule='@daily',
    catchup=False
) as dag:

    transfer_data = PythonOperator(
        task_id='extract_transform_load',
        python_callable=etl_postgres_to_onedrive
    )
