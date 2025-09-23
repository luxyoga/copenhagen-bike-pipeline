import os, io, requests, pandas as pd
from datetime import datetime, timezone

SOURCE_URL = os.getenv("SOURCE_URL", "")  # set this in .env or compose
OUT_DIR = "/opt/airflow/data/raw"

def run():
    if not SOURCE_URL:
        raise RuntimeError("SOURCE_URL missing (set env var)")
    
    print(f"Fetching data from: {SOURCE_URL}")
    r = requests.get(SOURCE_URL, timeout=60)
    r.raise_for_status()
    
    # Try to read as CSV first, with flexible encoding
    try:
        df = pd.read_csv(io.BytesIO(r.content), encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(io.BytesIO(r.content), encoding='latin-1')
        except Exception as e:
            print(f"Failed to read CSV with utf-8 and latin-1 encoding: {e}")
            raise
    
    print(f"Successfully loaded {len(df)} rows with columns: {list(df.columns)}")
    print(f"First few rows:\n{df.head()}")
    
    # Ensure we have some expected columns for traffic data
    expected_cols = ['timestamp', 'count', 'counter_id', 'location', 'bike', 'car', 'vehicle']
    found_cols = [col for col in expected_cols if col.lower() in [c.lower() for c in df.columns]]
    print(f"Found expected columns: {found_cols}")

    ts = datetime.now(timezone.utc).strftime("%Y%m%d")
    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, f"cph_traffic_raw_{ts}.csv")
    df.to_csv(out_path, index=False)
    print(f"Wrote {out_path} ({len(df)} rows)")

if __name__ == "__main__":
    run()