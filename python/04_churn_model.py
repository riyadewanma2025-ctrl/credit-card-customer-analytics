from pathlib import Path

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# ============================================================
# CREDIT CARD CUSTOMER INTELLIGENCE & CHURN ANALYTICS
# STEP 4: CHURN PREDICTION MODEL
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "customer_analysis.csv"
OUTPUT_PATH = BASE_DIR / "data" / "churn_predictions.csv"

# ------------------------------------------------------------
# 1. LOAD DATA
# ------------------------------------------------------------

df = pd.read_csv(DATA_PATH)

print("=" * 70)
print("CUSTOMER CHURN PREDICTION")
print("=" * 70)

# ------------------------------------------------------------
# 2. CREATE TARGET VARIABLE
# ------------------------------------------------------------

df["Attrition"] = (
    df["Attrition_Flag"]
    .map({
        "Existing Customer": 0,
        "Attrited Customer": 1
    })
)

# ------------------------------------------------------------
# 3. SELECT FEATURES
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

print(f"\nCustomers: {len(df):,}")
print(f"Features: {len(features)}")
print(f"Attrition rate: {y.mean() * 100:.2f}%")

# ------------------------------------------------------------
# 4. TRAIN / TEST SPLIT
# ------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"\nTraining observations: {len(X_train):,}")
print(f"Testing observations: {len(X_test):,}")

# ------------------------------------------------------------
# 5. PREPROCESSING
# ------------------------------------------------------------

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", __import__("sklearn").preprocessing.OneHotEncoder(
        handle_unknown="ignore"
    ))
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric_features),
    ("categorical", categorical_pipeline, categorical_features)
])

# ------------------------------------------------------------
# 6. LOGISTIC REGRESSION MODEL
# ------------------------------------------------------------

model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        random_state=42
    ))
])

# ------------------------------------------------------------
# 7. TRAIN MODEL
# ------------------------------------------------------------

print("\nTraining logistic regression model...")

model.fit(X_train, y_train)

print("Model training complete.")

# ------------------------------------------------------------
# 8. PREDICTIONS
# ------------------------------------------------------------

y_pred = model.predict(X_test)
y_probability = model.predict_proba(X_test)[:, 1]

# ------------------------------------------------------------
# 9. MODEL PERFORMANCE
# ------------------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_probability)

print("\n" + "=" * 70)
print("MODEL PERFORMANCE")
print("=" * 70)

print(f"\nAccuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")
print(f"ROC-AUC:   {roc_auc:.4f}")

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["Existing Customer", "Attrited Customer"]
))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ------------------------------------------------------------
# 10. FEATURE IMPORTANCE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("MODEL DRIVERS")
print("=" * 70)

preprocessor_fitted = model.named_steps["preprocessor"]
classifier = model.named_steps["classifier"]

feature_names = preprocessor_fitted.get_feature_names_out()

coefficients = classifier.coef_[0]

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Coefficient": coefficients,
    "Absolute_Impact": np.abs(coefficients)
})

importance_df = importance_df.sort_values(
    "Absolute_Impact",
    ascending=False
)

print("\nTop 15 model drivers:")
print(
    importance_df.head(15).to_string(index=False)
)

# ------------------------------------------------------------
# 11. SAVE FEATURE IMPORTANCE
# ------------------------------------------------------------

importance_df.to_csv(
    BASE_DIR / "data" / "model_feature_importance.csv",
    index=False
)

# ------------------------------------------------------------
# 12. SAVE PREDICTIONS
# ------------------------------------------------------------

test_results = X_test.copy()

# Preserve customer identifier for downstream analytics
test_results["CLIENTNUM"] = df.loc[X_test.index, "CLIENTNUM"].values

test_results["Actual_Attrition"] = y_test.values

test_results["Predicted_Attrition"] = y_pred

test_results["Churn_Probability"] = y_probability

test_results.to_csv(
    OUTPUT_PATH,
    index=False
)

# ------------------------------------------------------------
# 13. HIGH-RISK CUSTOMERS
# ------------------------------------------------------------

high_risk = test_results[
    test_results["Churn_Probability"] >= 0.70
].copy()

print("\n" + "=" * 70)
print("HIGH-RISK CUSTOMER ANALYSIS")
print("=" * 70)

print(
    f"\nCustomers with predicted churn probability >= 70%: "
    f"{len(high_risk):,}"
)

if len(high_risk) > 0:

    print(
        f"Share of test population: "
        f"{len(high_risk) / len(test_results) * 100:.2f}%"
    )

    print(
        f"Actual attrition rate within high-risk group: "
        f"{high_risk['Actual_Attrition'].mean() * 100:.2f}%"
    )

# ------------------------------------------------------------
# COMPLETE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CHURN MODEL COMPLETE")
print("=" * 70)

print("\nFiles created:")
print("  - data/churn_predictions.csv")
print("  - data/model_feature_importance.csv")

