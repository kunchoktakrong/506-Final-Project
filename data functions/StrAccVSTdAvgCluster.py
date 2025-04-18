import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

fighters = pd.read_csv('../new_fighters.csv')

def convert_pct(x):
    if isinstance(x, str):
        x = x.replace('"', '').strip() 
        if '%' in x:
            try:
                return float(x.replace('%', '').strip())
            except Exception as e:
                print(f"Error converting {x}: {e}")
                return None
        else:
            try:
                return float(x)
            except Exception as e:
                print(f"Error converting {x}: {e}")
                return None
    return x

fighters['StrAcc'] = fighters['StrAcc'].apply(convert_pct)
fighters['TDAvg'] = pd.to_numeric(fighters['TDAvg'], errors='coerce')

fighters_clean = fighters.dropna(subset=['StrAcc', 'TDAvg']).copy()

fighters_clean = fighters_clean[(fighters_clean['StrAcc'] != 0) & 
                                (fighters_clean['TDAvg'] != 0) &
                                (fighters_clean['StrAcc'] != 100) &
                                (fighters_clean['TDAvg'] != 100)]

print("Clean data shape:", fighters_clean.shape)
print(fighters_clean[['name', 'StrAcc', 'TDAvg']].head())

scaler = StandardScaler()
X = scaler.fit_transform(fighters_clean[['StrAcc', 'TDAvg']])

k = 3
kmeans = KMeans(n_clusters=k, random_state=42)
fighters_clean['cluster'] = kmeans.fit_predict(X)

cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
print("Cluster Centers:")
print(pd.DataFrame(cluster_centers, columns=['StrAcc', 'TDAvg']))

plt.figure(figsize=(10, 6))
sns.scatterplot(data=fighters_clean, x='StrAcc', y='TDAvg', hue='cluster', palette='viridis', s=100, alpha=0.8)
plt.xlabel('Career Significant Strike Accuracy (%)')
plt.ylabel('Average Takedowns per 15 Minutes')
plt.title('Clustering Fighters: StrAcc vs. TDAvg')
plt.legend(title='Cluster')
plt.show()

'''
Cluster Centers:
      StrAcc     TDAvg
0  52.214689  7.113277
1  36.322785  1.670497
2  51.117207  1.738645
'''
