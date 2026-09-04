

import sqlite3
import pandas as pd
from pathlib import Path

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

csv_path = PROJECT_ROOT / "data" / "credit_card_customers.csv"
db_path = PROJECT_ROOT / "data" / "credit_card_analytics.db"

# ------------------------------------------------------------
# Load CSV
# ------------------------------------------------------------

df = pd.read_csv(csv_path)

# Remove model-output columns
df = df.loc[:, ~df.columns.str.startswith("Naive_Bayes_Classifier")]

print("=" * 70)
print("LOADING CUSTOMER DATA INTO SQLITE")
print("=" * 70)

print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")

# ------------------------------------------------------------
# Create database
# ------------------------------------------------------------

conn = sqlite3.connect(db_path)

df.to_sql(
    "customers",
    conn,
    if_exists="replace",
    index=False
)
# Load model/dashboard dataset
dashboard_path = PROJECT_ROOT / "data" / "executive_dashboard_data.csv"

dashboard_df = pd.read_csv(dashboard_path)

dashboard_df.to_sql(
    "dashboard",
    conn,
    if_exists="replace",
    index=False
)

print(f"Dashboard data loaded: {len(dashboard_df):,} rows")
print(f"\nDatabase created: {db_path}")

# ------------------------------------------------------------
# SQL files to execute
# ------------------------------------------------------------

sql_files = [
    PROJECT_ROOT / "sql" / "01_customer_profiling.sql",
    PROJECT_ROOT / "sql" / "02_attrition_analysis.sql",
    PROJECT_ROOT / "sql" / "03_customer_behavior.sql",
    PROJECT_ROOT / "sql" / "04_risk_analysis.sql"
]
result_number = 1

# ------------------------------------------------------------
# Execute SQL
# ------------------------------------------------------------

for sql_path in sql_files:

    print("\n" + "=" * 70)
    print(f"RUNNING: {sql_path.name}")
    print("=" * 70)

    with open(sql_path, "r") as f:
        sql_script = f.read()

    queries = [
        query.strip()
        for query in sql_script.split(";")
        if query.strip()
    ]

    for query in queries:

        print(f"\n--- QUERY {result_number} ---")

        result = pd.read_sql_query(query, conn)

        print(result.to_string(index=False))

        output_path = (
            PROJECT_ROOT
            / "data"
            / f"sql_result_{result_number}.csv"
        )

        result.to_csv(output_path, index=False)

        print(f"\nSaved: {output_path}")

        result_number += 1

conn.close()

print("\n" + "=" * 70)
print("SQL ANALYSIS COMPLETE")
print("=" * 70)