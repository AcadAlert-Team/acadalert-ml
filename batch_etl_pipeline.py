# batch_etl_pipeline.py
import pandas as pd
from supabase import create_client, Client
import os
import logging

logging.basicConfig(level=logging.INFO)

# Initialize Database Connection
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def extract_data() -> pd.DataFrame:
    """EXTRACT: Pull raw transactional attendance logs."""
    logging.info("Extracting raw attendance data...")
    response = supabase.table("attendance_logs").select("*").execute()
    return pd.DataFrame(response.data)

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """TRANSFORM: Clean, aggregate, and compute metrics using Pandas."""
    logging.info("Transforming data...")
    
    # 1. Handle missing values (Data Cleansing)
    df.fillna(0, inplace=True)
    
    # 2. Compute aggregated metrics (Feature Engineering)
    df['total_attended'] = df['cgip_attended'] + df['cd_attended'] + df['ieft_attended']
    df['overall_attendance_pct'] = (df['total_attended'] / 150) * 100 # Assuming 150 total classes
    
    # 3. Filter anomalies
    df = df[df['overall_attendance_pct'] <= 100.0]
    
    # 4. Prepare for staging schema
    transformed_df = df[['student_id', 'overall_attendance_pct']]
    return transformed_df

def load_data(df: pd.DataFrame):
    """LOAD: Push transformed data to analytics staging table via UPSERT."""
    logging.info("Loading data into analytics_staging...")
    records = df.to_dict(orient='records')
    
    # UPSERT guarantees pipeline idempotency
    data, count = supabase.table("analytics_staging").upsert(records).execute()
    logging.info(f"Successfully loaded {len(records)} records.")

if __name__ == "__main__":
    try:
        raw_df = extract_data()
        clean_df = transform_data(raw_df)
        load_data(clean_df)
    except Exception as e:
        logging.error(f"Pipeline Failed: {e}")
        # In a production environment, this would trigger an alert (PagerDuty/Slack)
