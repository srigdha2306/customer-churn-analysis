
from pathlib import Path
import sqlite3
import pandas as pd

project_dir = Path(__file__).resolve().parents[1]

csv_path = (
    project_dir
    / "data"
    / "processed"
    / "telco_churn_cleaned.csv"
)

db_path = (
    project_dir
    / "data"
    / "processed"
    / "churn.db"
)

df = pd.read_csv(csv_path)

with sqlite3.connect(db_path) as connection:
    df.to_sql(
        "customers",
        connection,
        if_exists="replace",
        index=False
    )

    result = connection.execute(
        "SELECT COUNT(*) FROM customers"
    ).fetchone()

    print("Database created successfully!")
    print(f"Customers imported: {result[0]}")
    print(f"Database location: {db_path}")
