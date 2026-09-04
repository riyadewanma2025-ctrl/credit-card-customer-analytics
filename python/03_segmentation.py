from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# ============================================================
# CREDIT CARD CUSTOMER INTELLIGENCE & CHURN ANALYTICS
# STEP 3: CUSTOMER SEGMENTATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "customer_analysis.csv"
OUTPUT_PATH = BASE_DIR / "data" / "customer_segments.csv"
CHART_PATH = BASE_DIR / "dashboard"

CHART_PATH.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# 1. LOAD DATA
# ------------------------------------------------------------

df = pd.read_csv(DATA_PATH)

print("=" * 70)
print("CUSTOMER SEGMENTATION")
print("=" * 70)

print(f"\nCustomers analyzed: {len(df):,}")

# ------------------------------------------------------------
# 2. SELECT CUSTOMER BEHAVIOR VARIABLES
# ------------------------------------------------------------

features = [
    "Credit_Limit",
    "Total_Revolving_Bal",
    "Total_Trans_Amt",
    "Total_Trans_Ct",
    "Avg_Utilization_Ratio",
    "Months_Inactive_12_mon",
    "Total_Relationship_Count"
]

X = df[features].copy()

print("\nSegmentation variables:")
for feature in features:
    print(f"  - {feature}")

# ------------------------------------------------------------
# 3. STANDARDIZE FEATURES
# ------------------------------------------------------------

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# ------------------------------------------------------------
# 4. FIND BEST NUMBER OF CLUSTERS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TESTING CLUSTER COUNTS")
print("=" * 70)

silhouette_results = {}

for k in range(2, 7):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(X_scaled)

    score = silhouette_score(X_scaled, labels)

    silhouette_results[k] = score

    print(f"K = {k} | Silhouette Score = {score:.4f}")

# ------------------------------------------------------------
# 5. SELECT BEST CLUSTER COUNT
# ------------------------------------------------------------

best_k = max(
    silhouette_results,
    key=silhouette_results.get
)

print(f"\nBest number of clusters: {best_k}")

# ------------------------------------------------------------
# 6. FIT FINAL MODEL
# ------------------------------------------------------------

kmeans = KMeans(
    n_clusters=best_k,
    random_state=42,
    n_init=10
)

df["Cluster"] = kmeans.fit_predict(X_scaled)

# ------------------------------------------------------------
# 7. CLUSTER PROFILE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CUSTOMER SEGMENT PROFILES")
print("=" * 70)

cluster_profile = df.groupby("Cluster")[features].mean()

cluster_sizes = df["Cluster"].value_counts().sort_index()

print("\nCluster sizes:")
print(cluster_sizes)

print("\nCluster averages:")
print(cluster_profile.round(2))

# ------------------------------------------------------------
# 8. ATTRITION BY SEGMENT
# ------------------------------------------------------------

if "Attrition" in df.columns:

    attrition_by_cluster = (
        df.groupby("Cluster")["Attrition"]
        .mean()
        .mul(100)
        .round(2)
    )

    print("\nAttrition rate by cluster:")
    print(attrition_by_cluster)

    cluster_profile["Attrition_Rate"] = attrition_by_cluster

# ------------------------------------------------------------
# 9. SAVE CUSTOMER SEGMENTS
# ------------------------------------------------------------

df.to_csv(
    OUTPUT_PATH,
    index=False
)

# ------------------------------------------------------------
# 10. SAVE CLUSTER PROFILE
# ------------------------------------------------------------

profile_path = BASE_DIR / "data" / "cluster_profiles.csv"

cluster_profile.to_csv(profile_path)

# ------------------------------------------------------------
# 11. SILHOUETTE SCORE VISUALIZATION
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    list(silhouette_results.keys()),
    list(silhouette_results.values()),
    marker="o"
)

plt.title("Silhouette Score by Number of Clusters")
plt.xlabel("Number of Clusters")
plt.ylabel("Silhouette Score")
plt.xticks(list(silhouette_results.keys()))
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    CHART_PATH / "06_silhouette_scores.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# 12. SEGMENT SIZE VISUALIZATION
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

cluster_sizes.plot(kind="bar")

plt.title("Customer Distribution by Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    CHART_PATH / "07_customer_segments.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# COMPLETE
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("SEGMENTATION COMPLETE")
print("=" * 70)

print("\nFiles created:")
print("  - data/customer_segments.csv")
print("  - data/cluster_profiles.csv")
print("  - dashboard/06_silhouette_scores.png")
print("  - dashboard/07_customer_segments.png")

