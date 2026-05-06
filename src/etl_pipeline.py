import pandas as pd
import sqlalchemy as sa
import os

RAW_DATA_PATH = 'data/raw/time_series_60min_singleindex.csv'
DB_PATH = 'sqlite:///data/processed/energy_tracker.db'

def run_etl():
    print("Starting the Energy ETL Pipeline...")

    # --- PHASE 1: EXTRACT ---
    # We only want DE columns. We use 'usecols' to keep it fast.
    # First, we just read the headers to find which columns have "DE"
    headers = pd.read_csv(RAW_DATA_PATH, nrows=0).columns
    de_cols = [c for c in headers if "DE" in c or 'utc_timestamp' in c]

    print(f"Extracting {len(de_cols)} columns from raw CSV...")
    df = pd.read_csv(RAW_DATA_PATH, usecols=de_cols)

    # --- PHASE 2: TRANSFORM (Cleaning) ---
    print("Transforming and Cleaning data...")

    # Ensuring the timestamp is a real date/time object
    df['utc_timestamp'] = pd.to_datetime(df['utc_timestamp'])

    # 41 columns into 3 columns: Timestamp, Sensor_Name, and Value
    df_long = df.melt(id_vars=['utc_timestamp'], var_name='metric', value_name='value')

    # Fixing the Gaps (Smart Interpolation)
    # limit=2 means we only fill a gap if it's 2 hours or less.
    # This fixes sensor glitches but preserves the "big holes" like the 2015-2018 price gap.
    print("Applying smart interpolation (limiting to small gaps)...")
    
    df_long['value'] = df_long.groupby('metric')['value'].transform(
        lambda x: x.interpolate(method='linear', limit=2)
    )

    # --- PHASE 3: LOAD (The Database) ---
    print("Loading data into SQLite Database...")
    
    # Creating the connection to the database (creates the file if it doesn't exist!)
    engine = sa.create_engine(DB_PATH)
    
    # Push the data to a table called 'germany_energy'
    # 'if_exists=replace' means if we run it again, it starts fresh
    df_long.to_sql('germany_energy', engine, if_exists='replace', index=False)

    print("ETL Complete! Your database is ready at data/processed/energy_tracker.db")

if __name__ == "__main__":
    run_etl()