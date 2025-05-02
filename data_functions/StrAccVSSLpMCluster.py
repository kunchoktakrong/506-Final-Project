import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px

# build absolute path to scraping/new_fighters.csv
base_dir = os.path.dirname(__file__)  # data_functions/
fighters_fp = os.path.abspath(os.path.join(base_dir, "..", "scraping", "new_fighters.csv"))

# Load and clean
fighters = pd.read_csv(fighters_fp)

def convert_pct(x):
    if isinstance(x, str):
        x = x.replace('"', '').strip() 
        if '%' in x:
            try:
                return float(x.replace('%', '').strip())
            except:
                return None
        try:
            return float(x)
        except:
            return None
    return x

fighters['StrAcc'] = fighters['StrAcc'].apply(convert_pct)
fighters['SLpM']   = pd.to_numeric(fighters['SLpM'], errors='coerce')

# drop zeros & extremes
fighters_clean = fighters.dropna(subset=['StrAcc', 'SLpM'])
fighters_clean = fighters_clean[
    (fighters_clean['StrAcc'] != 0) &
    (fighters_clean['SLpM']    != 0) &
    (fighters_clean['StrAcc']  != 100) &
    (fighters_clean['SLpM']    != 100)
]

print("Clean data shape:", fighters_clean.shape)
print(fighters_clean[['name', 'StrAcc', 'SLpM']].head())

# standardize & cluster
scaler = StandardScaler()
X      = scaler.fit_transform(fighters_clean[['StrAcc', 'SLpM']])
k      = 4
kmeans = KMeans(n_clusters=k, random_state=42).fit(X)
fighters_clean['cluster'] = kmeans.labels_

# interactive plot
fig = px.scatter(
    fighters_clean,
    x='StrAcc', y='SLpM',
    color='cluster', hover_name='name',
    title='Interactive Clustering: StrAcc vs. SLpM',
    labels={
      'StrAcc':'Significant Strike Accuracy (%)',
      'SLpM':'Significant Strikes Landed per Minute',
      'cluster':'Cluster'
    }
)
fig.update_traces(marker=dict(size=8, opacity=0.7))
fig.show()

# cluster centers (back to original units)
centers = scaler.inverse_transform(kmeans.cluster_centers_)
print("Cluster Centers:")
print(pd.DataFrame(centers, columns=['StrAcc','SLpM']))

# static seaborn plot
plt.figure(figsize=(10,6))
sns.scatterplot(
    data=fighters_clean, x='StrAcc', y='SLpM',
    hue='cluster', palette='viridis', s=100, alpha=0.8
)
plt.xlabel('Career Significant Strike Accuracy (%)')
plt.ylabel('Significant Strikes Landed per Minute')
plt.title('Clustering Fighters: StrAcc vs. SLpM')
plt.legend(title='Cluster')
plt.tight_layout()
plt.show()
