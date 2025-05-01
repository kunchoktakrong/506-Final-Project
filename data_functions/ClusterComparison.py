import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

matches = pd.read_csv('../new_matches.csv')
clusters = pd.read_csv('fighter_clusters.csv')  

matches = matches.merge(clusters.rename(columns={'name': 'fighter_1', 'cluster': 'cluster_1'}), on='fighter_1', how='left')
matches = matches.merge(clusters.rename(columns={'name': 'fighter_2', 'cluster': 'cluster_2'}), on='fighter_2', how='left')

matches['label'] = (matches['fighter_1_result'] == 'W').astype(int)

matches = matches.dropna(subset=['cluster_1', 'cluster_2'])

matches['cluster_1'] = matches['cluster_1'].astype(int)
matches['cluster_2'] = matches['cluster_2'].astype(int)

pivot = pd.pivot_table(matches, values='label', index='cluster_1', columns='cluster_2', aggfunc='mean')

plt.figure(figsize=(8, 6))
sns.heatmap(pivot, annot=True, fmt=".2f", cmap='coolwarm', linewidths=0.5, square=True)
plt.title("Fighter 1 Win Rate by Cluster Matchup")
plt.xlabel("Fighter 2 Cluster")
plt.ylabel("Fighter 1 Cluster")
plt.tight_layout()
plt.show()
