import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# build absolute paths
base_dir    = os.path.dirname(__file__)
matches_fp  = os.path.abspath(os.path.join(base_dir, "..", "scraping", "new_matches.csv"))
clusters_fp = os.path.abspath(os.path.join(base_dir,       "fighter_clusters.csv"))

# load
matches = pd.read_csv(matches_fp)
clusters = pd.read_csv(clusters_fp)

# merge cluster labels
matches = matches.merge(
    clusters.rename(columns={'name':'fighter_1','cluster':'cluster_1'}),
    on='fighter_1', how='left'
).merge(
    clusters.rename(columns={'name':'fighter_2','cluster':'cluster_2'}),
    on='fighter_2', how='left'
)

# 1 if fighter_1 won
matches['label'] = (matches['fighter_1_result']=="W").astype(int)
matches = matches.dropna(subset=['cluster_1','cluster_2'])\
                 .astype({'cluster_1':int,'cluster_2':int})

# pivot table of win‐rates
pivot = matches.pivot_table(
    values='label',
    index='cluster_1',
    columns='cluster_2',
    aggfunc='mean'
)

# plot
plt.figure(figsize=(8,6))
sns.heatmap(
    pivot, annot=True, fmt=".2f",
    cmap='coolwarm', linewidths=0.5, square=True
)
plt.title("Fighter 1 Win Rate by Cluster Matchup")
plt.xlabel("Fighter 2 Cluster")
plt.ylabel("Fighter 1 Cluster")
plt.tight_layout()
plt.show()
