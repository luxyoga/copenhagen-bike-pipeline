#!/usr/bin/env python3
"""
Download real Copenhagen cycling data from Kaggle

This script downloads the authentic Copenhagen bike traffic data
from Kaggle and processes it for the pipeline.
"""

import kagglehub
import os
import pandas as pd
from datetime import datetime

def download_and_process_kaggle_data():
    """Download and process the real Copenhagen cycling data from Kaggle"""
    print("🚴‍♂️ DOWNLOADING REAL COPENHAGEN CYCLING DATA")
    print("=" * 80)
    
    # Define the dataset and destination
    dataset_id = "emilhvitfeldt/bike-traffic-counts-in-copenhagen"
    
    # Download the dataset
    print(f"📥 Downloading dataset: {dataset_id}")
    dataset_path = kagglehub.dataset_download(dataset_id)
    print(f"✅ Dataset downloaded to: {dataset_path}")
    
    # Process the downloaded files
    output_dir = "data/curated"
    os.makedirs(output_dir, exist_ok=True)
    
    csv_files = [f for f in os.listdir(dataset_path) if f.endswith('.csv')]
    print(f"📁 Files in dataset: {os.listdir(dataset_path)}")
    print(f"📊 CSV files found: {csv_files}")

    for csv_file in csv_files:
        file_path = os.path.join(dataset_path, csv_file)
        print(f"\n📊 Processing: {file_path}")
        df = pd.read_csv(file_path)
        print(f"   📊 Rows: {len(df):,}")
        print(f"   📋 Columns: {list(df.columns)}")
        print(f"   📊 Sample data:\n{df.head(3)}")

        # Save processed data
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file_path = os.path.join(output_dir, f"real_copenhagen_data_{ts}.csv")
        df.to_csv(output_file_path, index=False)
        print(f"   ✅ Saved: {output_file_path}")
    
    print("\n🎉 SUCCESS! Real Copenhagen cycling data downloaded!")
    print("   📊 Data is now in data/curated/")
    print("   🔄 Ready to integrate into pipeline")
    print("   ✅ REAL DATA RESTORED!")

if __name__ == "__main__":
    download_and_process_kaggle_data()
