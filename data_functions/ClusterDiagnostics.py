import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

# Determine file path for fighters data relative to this script
base_dir = os.path.dirname(__file__)
fighters_fp = os.path.abspath(
    os.path.join(base_dir, '..', 'scraping', 'new_fighters.csv')
)

# Load and clean fighter stats
fighters = pd.read_csv(fighters_fp)

def convert_pct(x):
    if isinstance(x, str):
        x = x.replace('"', '').strip()
        if '%' in x:
            try:
                return float(x.replace('%', ''))
            except:
                return None
        try:
            return float(x)
        except:
            return None
    return x

fighters['StrAcc'] = fighters['StrAcc'].apply(convert_pct)
fighters['TDAvg'] = pd.to_numeric(fighters['TDAvg'], errors='coerce')

# Filter out invalid values
fighters_clean = fighters.dropna(subset=['StrAcc', 'TDAvg']).copy()
fighters_clean = fighters_clean[
    (fighters_clean['StrAcc'] != 0) &
    (fighters_clean['TDAvg']  != 0) &
    (fighters_clean['StrAcc'] != 100) &
    (fighters_clean['TDAvg']  != 100)
]

# Standardize features
scaler = StandardScaler()
X = scaler.fit_transform(fighters_clean[['StrAcc', 'TDAvg']])

# Compute inertia and silhouette scores for range of k
inertias = []
sil_scores = []
k_range = range(2, 11)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X)
    inertias.append(kmeans.inertia_)
    sil_scores.append(silhouette_score(X, labels))

# Plot elbow and silhouette plots
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(k_range, inertias, marker='o')
plt.title('Elbow Plot')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')

plt.subplot(1, 2, 2)
plt.plot(k_range, sil_scores, marker='o')
plt.title('Silhouette Score')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Score')

plt.tight_layout()
plt.show()
