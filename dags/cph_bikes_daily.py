"""
Copenhagen Bike Data Pipeline DAG

This DAG orchestrates the daily processing of Copenhagen cycling data:
1. Ingests real cycling data from Kaggle
2. Transforms and processes the data
3. Makes it available for the Streamlit dashboard

Author: lux
Schedule: Daily at 04:10 UTC
"""

from datetime import datetime, timedelta, timezone
from airflow import DAG
from airflow.operators.python import PythonOperator
import os
import pandas as pd

# Default arguments for the DAG
default_args = {
    "owner": "lux",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
    "email_on_retry": False,
}

with DAG(
    dag_id="cph_bike_daily",
    start_date=datetime(2025, 9, 1),
    schedule_interval="10 4 * * *",   # 04:10 UTC daily
    catchup=False,
    default_args=default_args,
    tags=["copenhagen","bikes","spark"]
) as dag:

    def ingest_data():
        """
        Ingest Copenhagen cycling data from the curated dataset.
        
        This task loads the processed Copenhagen cycling data with weather
        information and saves it to the raw data directory for processing.
        
        Returns:
            str: Path to the ingested raw data file
        """
        OUT_DIR = "/opt/airflow/data/raw"
        REALISTIC_DATA = "/opt/airflow/data/curated/real_copenhagen_data_with_weather_fixed.csv"
        
        print(f"🚴‍♂️ Ingesting Copenhagen cycling data from: {REALISTIC_DATA}")
        
        if not os.path.exists(REALISTIC_DATA):
            raise RuntimeError(f"❌ Data source not found: {REALISTIC_DATA}")
        
        # Read the processed data
        df = pd.read_csv(REALISTIC_DATA)
        print(f"✅ Successfully loaded {len(df):,} rows with columns: {list(df.columns)}")
        print(f"📊 Data preview:\n{df.head()}")

        # Save to raw directory with timestamp
        ts = datetime.now(timezone.utc).strftime("%Y%m%d")
        os.makedirs(OUT_DIR, exist_ok=True)
        out_path = os.path.join(OUT_DIR, f"cph_traffic_raw_{ts}.csv")
        df.to_csv(out_path, index=False)
        print(f"💾 Saved raw data to: {out_path} ({len(df):,} rows)")
        return out_path

    ingest = PythonOperator(
        task_id="ingest_csv_to_raw",
        python_callable=ingest_data,
    )

    def transform_data():
        """
        Transform and process the raw cycling data.
        
        This task processes the raw cycling data, applies transformations,
        and saves the processed data to the curated directory for the dashboard.
        
        Returns:
            str: Path to the processed data file
        """
        RAW_DIR = "/opt/airflow/data/raw"
        CUR_DIR = "/opt/airflow/data/curated"
        
        os.makedirs(CUR_DIR, exist_ok=True)
        
        # Find the latest raw file
        raw_files = [f for f in os.listdir(RAW_DIR) if f.startswith("cph_traffic_raw_") and f.endswith(".csv")]
        if not raw_files:
            raise RuntimeError("❌ No raw data files found in {RAW_DIR}")
        
        latest_file = sorted(raw_files)[-1]
        raw_path = os.path.join(RAW_DIR, latest_file)
        
        print(f"🔄 Processing raw data: {raw_path}")
        
        # Read and process the data
        df = pd.read_csv(raw_path)
        print(f"📊 Loaded {len(df):,} records for processing")
        
        # Apply data transformations
        # Add processing timestamp
        df['processed_at'] = datetime.now(timezone.utc).isoformat()
        
        # Save processed data with timestamp
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        curated_path = os.path.join(CUR_DIR, f"processed_data_{ts}.csv")
        df.to_csv(curated_path, index=False)
        
        print(f"✅ Processed data saved to: {curated_path}")
        print(f"📈 Data ready for dashboard visualization")
        return curated_path

    transform = PythonOperator(
        task_id="spark_transform_to_parquet",
        python_callable=transform_data,
    )

    ingest >> transform