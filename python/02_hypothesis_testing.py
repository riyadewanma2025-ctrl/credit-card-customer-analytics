from pathlib import Path
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# ============================================================
# CREDIT CARD CUSTOMER INTELLIGENCE & CHURN ANALYTICS
# STEP 2: STATISTICAL HYPOTHESIS TESTING
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "customer_analysis.csv"

df = pd.read_csv(DATA_PATH)

# ------------------------------------------------------------
# Convert customer status to binary target
# ------------------------------------------------------------

df["Attrition"] = (
    df["Attrition_Flag"]
    .map({
        "Existing Customer": 0,
        "Attrited Customer": 1
    })
)

existing = df[df["Attrition"] == 0]
attrited = df[df["Attrition"] == 1]

print("=" * 70)
print("STATISTICAL HYPOTHESIS TESTING")
print("=" * 70)

print(f"\nExisting customers: {len(existing):,}")
print(f"Attrited customers: {len(attrited):,}")

# ------------------------------------------------------------
# Define hypotheses
# ------------------------------------------------------------

tests = {

    "Transaction Count": {
        "column": "Total_Trans_Ct",
        "hypothesis": "Attrited customers have different transaction counts."
    },

    "Months Inactive": {
        "column": "Months_Inactive_12_mon",
        "hypothesis": "Attrited customers have higher inactivity."
    },

    "Customer Contacts": {
        "column": "Contacts_Count_12_mon",
        "hypothesis": "Attrited customers have more customer-service contacts."
    }
}

results = []

# ------------------------------------------------------------
# Run Welch's independent samples t-test
# ------------------------------------------------------------

for test_name, details in tests.items():

    column = details["column"]

    existing_values = existing[column].dropna()
    attrited_values = attrited[column].dropna()

    statistic, p_value = ttest_ind(
        existing_values,
        attrited_values,
        equal_var=False
    )

    existing_mean = existing_values.mean()
    attrited_mean = attrited_values.mean()

    difference = attrited_mean - existing_mean

    if p_value < 0.05:
        conclusion = "Statistically significant"
    else:
        conclusion = "Not statistically significant"

    print("\n" + "-" * 70)
    print(test_name)
    print("-" * 70)

    print(f"Hypothesis: {details['hypothesis']}")
    print(f"\nExisting customer mean: {existing_mean:.4f}")
    print(f"Attrited customer mean: {attrited_mean:.4f}")
    print(f"Difference: {difference:.4f}")
    print(f"T-statistic: {statistic:.4f}")
    print(f"P-value: {p_value:.10f}")
    print(f"Conclusion: {conclusion}")

    results.append({
        "Metric": test_name,
        "Existing_Mean": existing_mean,
        "Attrited_Mean": attrited_mean,
        "Difference": difference,
        "T_Statistic": statistic,
        "P_Value": p_value,
        "Significant_at_5pct": p_value < 0.05
    })

# ------------------------------------------------------------
# Save results
# ------------------------------------------------------------

results_df = pd.DataFrame(results)

results_df.to_csv(
    BASE_DIR / "data" / "hypothesis_test_results.csv",
    index=False
)

print("\n" + "=" * 70)
print("HYPOTHESIS TESTING COMPLETE")
print("=" * 70)

print("\nResults saved to:")
print(BASE_DIR / "data" / "hypothesis_test_results.csv")

print("\nSummary:")
print(results_df.to_string(index=False))
