import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

fighters = pd.read_csv('scraping/new_fighters.csv')

def convert_pct(x):
    if isinstance(x, str):
        x = x.replace('"', '').strip()
        if '%' in x:
            return float(x.replace('%', ''))
        try:
            return float(x)
        except:
            return None
    return x

fighters['StrAcc'] = fighters['StrAcc'].apply(convert_pct)
fighters['TDAvg'] = pd.to_numeric(fighters['TDAvg'], errors='coerce')

fighters_clean = fighters.dropna(subset=['StrAcc', 'TDAvg']).copy()
fighters_clean = fighters_clean[
    (fighters_clean['StrAcc'] != 0) & (fighters_clean['TDAvg'] != 0) &
    (fighters_clean['StrAcc'] != 100) & (fighters_clean['TDAvg'] != 100)
]

scaler = StandardScaler()
X = scaler.fit_transform(fighters_clean[['StrAcc', 'TDAvg']])

dbscan = DBSCAN(eps=0.5, min_samples=10)
labels = dbscan.fit_predict(X)
fighters_clean['cluster'] = labels

plt.figure(figsize=(10, 6))
sns.scatterplot(data=fighters_clean, x='StrAcc', y='TDAvg', hue='cluster', palette='tab10', s=80, alpha=0.8)
plt.title('DBSCAN Clustering: StrAcc vs. TDAvg')
plt.xlabel('Career Significant Strike Accuracy (%)')
plt.ylabel('Average Takedowns per 15 Minutes')
plt.legend(title='Cluster')
plt.grid(True)
plt.show()
