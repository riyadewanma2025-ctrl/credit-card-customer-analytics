from pathlib import Path
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression

# ============================================================
# CREDIT CARD CUSTOMER INTELLIGENCE & CHURN ANALYTICS
# STEP 5: EXECUTIVE DASHBOARD DATASET
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "customer_analysis.csv"
SEGMENT_PATH = BASE_DIR / "data" / "customer_segments.csv"
OUTPUT_PATH = BASE_DIR / "data" / "executive_dashboard_data.csv"

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

df = pd.read_csv(DATA_PATH)
segments = pd.read_csv(SEGMENT_PATH)

# ------------------------------------------------------------
# TARGET
# ------------------------------------------------------------

df["Attrition"] = (
    df["Attrition_Flag"]
    .map({
        "Existing Customer": 0,
        "Attrited Customer": 1
    })
)

# ------------------------------------------------------------
# FEATURES
# ------------------------------------------------------------

numeric_features = [
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
    "Avg_Utilization_Ratio"
]

categorical_features = [
    "Gender",
    "Education_Level",
    "Marital_Status",
    "Income_Category",
    "Card_Category"
]

features = numeric_features + categorical_features

X = df[features]
y = df["Attrition"]

# ------------------------------------------------------------
# TRAIN / TEST SPLIT
# ------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ------------------------------------------------------------
# PREPROCESSING
# ------------------------------------------------------------

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric_features),
    ("categorical", categorical_pipeline, categorical_features)
])

# ------------------------------------------------------------
# MODEL
# ------------------------------------------------------------

model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        random_state=42
    ))
])

model.fit(X_train, y_train)

# ------------------------------------------------------------
# SCORE ALL CUSTOMERS
# ------------------------------------------------------------

all_probabilities = model.predict_proba(X)[:, 1]

dashboard = df.copy()

dashboard["Churn_Probability"] = all_probabilities

dashboard["Predicted_Attrition"] = (
    dashboard["Churn_Probability"] >= 0.50
).astype(int)

# ------------------------------------------------------------
# ADD SEGMENT
# ------------------------------------------------------------

segment_lookup = segments[
    ["CLIENTNUM", "Cluster"]
].copy()

dashboard = dashboard.merge(
    segment_lookup,
    on="CLIENTNUM",
    how="left"
)

dashboard["Customer_Segment"] = dashboard["Cluster"].map({
    0: "Core Portfolio",
    1: "High-Value Active"
})

# ------------------------------------------------------------
# RISK CATEGORY
# ------------------------------------------------------------

def risk_category(probability):

    if probability >= 0.70:
        return "High Risk"

    elif probability >= 0.40:
        return "Medium Risk"

    else:
        return "Low Risk"


dashboard["Risk_Category"] = dashboard[
    "Churn_Probability"
].apply(risk_category)

# ------------------------------------------------------------
# ENGAGEMENT
# ------------------------------------------------------------

def engagement_category(transaction_count):

    if transaction_count >= 80:
        return "Highly Engaged"

    elif transaction_count >= 50:
        return "Moderately Engaged"

    else:
        return "Low Engagement"


dashboard["Engagement_Category"] = dashboard[
    "Total_Trans_Ct"
].apply(engagement_category)

# ------------------------------------------------------------
# UTILIZATION
# ------------------------------------------------------------

def utilization_category(utilization):

    if utilization >= 0.50:
        return "High Utilization"

    elif utilization >= 0.20:
        return "Moderate Utilization"

    else:
        return "Low Utilization"


dashboard["Utilization_Category"] = dashboard[
    "Avg_Utilization_Ratio"
].apply(utilization_category)

# ------------------------------------------------------------
# FINAL COLUMNS
# ------------------------------------------------------------

dashboard_columns = [
    "CLIENTNUM",
    "Attrition_Flag",
    "Attrition",
    "Customer_Segment",
    "Risk_Category",
    "Engagement_Category",
    "Utilization_Category",
    "Customer_Age",
    "Gender",
    "Income_Category",
    "Card_Category",
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
    "Churn_Probability",
    "Predicted_Attrition"
]

dashboard = dashboard[
    [c for c in dashboard_columns if c in dashboard.columns]
]

# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

dashboard.to_csv(
    OUTPUT_PATH,
    index=False
)

# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

print("=" * 70)
print("EXECUTIVE DASHBOARD DATASET")
print("=" * 70)

print(f"\nTotal customers scored: {len(dashboard):,}")

print("\nCustomer segments:")
print(dashboard["Customer_Segment"].value_counts())

print("\nRisk categories:")
print(dashboard["Risk_Category"].value_counts())

print("\nAverage predicted churn probability:")
print(
    f"{dashboard['Churn_Probability'].mean() * 100:.2f}%"
)

print("\nHigh-risk customers:")
print(
    (dashboard["Risk_Category"] == "High Risk").sum()
)

print("\nHigh-risk attrition rate:")
high_risk = dashboard[
    dashboard["Risk_Category"] == "High Risk"
]

print(
    f"{high_risk['Attrition'].mean() * 100:.2f}%"
)

print("\nDashboard dataset saved to:")
print(OUTPUT_PATH)

print("\n" + "=" * 70)
print("DASHBOARD DATASET COMPLETE")
print("=" * 70)
