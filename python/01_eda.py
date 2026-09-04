import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ============================================================
# CREDIT CARD CUSTOMER INTELLIGENCE & CHURN ANALYTICS
# STEP 1: EXPLORATORY DATA ANALYSIS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "credit_card_customers.csv"
OUTPUT_PATH = BASE_DIR / "data" / "customer_analysis.csv"
CHART_PATH = BASE_DIR / "dashboard"

Path(CHART_PATH).mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# 1. LOAD DATA
# ------------------------------------------------------------

df = pd.read_csv(DATA_PATH)

print("=" * 70)
print("CREDIT CARD CUSTOMER ANALYTICS")
print("=" * 70)

print(f"\nDataset shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

# ------------------------------------------------------------
# 2. REMOVE MODEL OUTPUT COLUMNS
# ------------------------------------------------------------

model_output_columns = [
    col for col in df.columns
    if col.startswith("Naive_Bayes_Classifier")
]

df = df.drop(columns=model_output_columns)

print("\nRemoved model-output columns:")
for col in model_output_columns:
    print(f"  - {col}")

print(f"\nFinal analytical dataset: {df.shape[0]:,} rows × {df.shape[1]} columns")

# ------------------------------------------------------------
# 3. DATA QUALITY CHECK
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("DATA QUALITY")
print("=" * 70)

print("\nMissing values:")
missing = df.isnull().sum()
print(missing[missing > 0] if missing.sum() > 0 else "No missing values found.")

print(f"\nDuplicate rows: {df.duplicated().sum()}")

print("\nData types:")
print(df.dtypes)

# ------------------------------------------------------------
# 4. ATTRITION ANALYSIS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CUSTOMER ATTRITION")
print("=" * 70)

attrition_counts = df["Attrition_Flag"].value_counts()
attrition_pct = df["Attrition_Flag"].value_counts(normalize=True) * 100

print("\nCustomer status:")
print(attrition_counts)

print("\nCustomer status percentage:")
print(attrition_pct.round(2))

# Create binary target
df["Attrition"] = (
    df["Attrition_Flag"]
    .map({
        "Existing Customer": 0,
        "Attrited Customer": 1
    })
)

print(f"\nOverall attrition rate: {df['Attrition'].mean() * 100:.2f}%")

# ------------------------------------------------------------
# 5. KEY BUSINESS METRICS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("KEY BUSINESS METRICS")
print("=" * 70)

metrics = {
    "Total Customers": len(df),
    "Attrition Rate (%)": df["Attrition"].mean() * 100,
    "Average Credit Limit": df["Credit_Limit"].mean(),
    "Average Revolving Balance": df["Total_Revolving_Bal"].mean(),
    "Average Transaction Amount": df["Total_Trans_Amt"].mean(),
    "Average Transaction Count": df["Total_Trans_Ct"].mean(),
    "Average Utilization Ratio": df["Avg_Utilization_Ratio"].mean(),
    "Average Months Inactive": df["Months_Inactive_12_mon"].mean(),
}

for metric, value in metrics.items():
    if isinstance(value, (int, np.integer)):
        print(f"{metric}: {value:,}")
    else:
        print(f"{metric}: {value:,.2f}")

# ------------------------------------------------------------
# 6. ATTRITION BY CUSTOMER BEHAVIOR
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("ATTRITION BY CUSTOMER BEHAVIOR")
print("=" * 70)

behavior_columns = [
    "Credit_Limit",
    "Total_Revolving_Bal",
    "Total_Trans_Amt",
    "Total_Trans_Ct",
    "Avg_Utilization_Ratio",
    "Months_Inactive_12_mon",
    "Contacts_Count_12_mon",
    "Total_Relationship_Count"
]

for column in behavior_columns:

    grouped = df.groupby("Attrition")[column].mean()

    print(f"\n{column}")
    print(f"  Existing customers: {grouped.get(0, np.nan):,.2f}")
    print(f"  Attrited customers: {grouped.get(1, np.nan):,.2f}")

# ------------------------------------------------------------
# 7. VISUALIZATION — ATTRITION
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

sns.countplot(
    data=df,
    x="Attrition_Flag"
)

plt.title("Customer Attrition Distribution")
plt.xlabel("Customer Status")
plt.ylabel("Number of Customers")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    f"{CHART_PATH}/01_attrition_distribution.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# 8. VISUALIZATION — TRANSACTION ACTIVITY
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))

sns.boxplot(
    data=df,
    x="Attrition_Flag",
    y="Total_Trans_Ct"
)

plt.title("Transaction Count by Customer Status")
plt.xlabel("Customer Status")
plt.ylabel("Total Transaction Count")
plt.tight_layout()

plt.savefig(
    f"{CHART_PATH}/02_transaction_count_attrition.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# 9. VISUALIZATION — UTILIZATION
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))

sns.boxplot(
    data=df,
    x="Attrition_Flag",
    y="Avg_Utilization_Ratio"
)

plt.title("Credit Utilization by Customer Status")
plt.xlabel("Customer Status")
plt.ylabel("Average Utilization Ratio")
plt.tight_layout()

plt.savefig(
    f"{CHART_PATH}/03_utilization_attrition.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# 10. VISUALIZATION — INACTIVITY
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))

sns.countplot(
    data=df,
    x="Months_Inactive_12_mon",
    hue="Attrition_Flag"
)

plt.title("Customer Attrition by Months Inactive")
plt.xlabel("Months Inactive in Last 12 Months")
plt.ylabel("Number of Customers")
plt.tight_layout()

plt.savefig(
    f"{CHART_PATH}/04_inactivity_attrition.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# 11. VISUALIZATION — CORRELATION
# ------------------------------------------------------------

numeric_columns = [
    "Customer_Age",
    "Dependent_count",
    "Months_on_book",
    "Total_Relationship_Count",
    "Months_Inactive_12_mon",
    "Contacts_Count_12_mon",
    "Credit_Limit",
    "Total_Revolving_Bal",
    "Avg_Open_To_Buy",
    "Total_Amt_Chng_Q4_Q1",
    "Total_Trans_Amt",
    "Total_Trans_Ct",
    "Total_Ct_Chng_Q4_Q1",
    "Avg_Utilization_Ratio",
    "Attrition"
]

correlation = df[numeric_columns].corr()

plt.figure(figsize=(13, 10))

sns.heatmap(
    correlation,
    annot=False,
    cmap="coolwarm",
    center=0
)

plt.title("Correlation Matrix — Customer & Credit Behavior")
plt.tight_layout()

plt.savefig(
    f"{CHART_PATH}/05_correlation_matrix.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# 12. SAVE ANALYTICAL DATASET
# ------------------------------------------------------------

df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\n" + "=" * 70)
print("EDA COMPLETE")
print("=" * 70)

print(f"\nAnalytical dataset saved to:")
print(OUTPUT_PATH)

print("\nCharts created:")
print("  01_attrition_distribution.png")
print("  02_transaction_count_attrition.png")
print("  03_utilization_attrition.png")
print("  04_inactivity_attrition.png")
print("  05_correlation_matrix.png")

print("\nNext step: statistical hypothesis testing.")
