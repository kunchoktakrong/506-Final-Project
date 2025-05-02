import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

base_dir    = os.path.dirname(__file__)
matches_fp  = os.path.abspath(os.path.join(base_dir, '..', 'scraping', 'new_matches.csv'))
clusters_fp = os.path.abspath(os.path.join(base_dir,        'fighter_clusters.csv'))

matches = pd.read_csv(matches_fp)
clusters = pd.read_csv(clusters_fp)

matches = matches.merge(
    clusters.rename(columns={'name': 'fighter_1', 'cluster': 'cluster_1'}),
    on='fighter_1', how='left'
)
matches = matches.merge(
    clusters.rename(columns={'name': 'fighter_2', 'cluster': 'cluster_2'}),
    on='fighter_2', how='left'
)

matches['label'] = (matches['fighter_1_result'] == 'W').astype(int)

matches = matches.dropna(subset=['cluster_1', 'cluster_2'])
matches['cluster_1'] = matches['cluster_1'].astype(int)
matches['cluster_2'] = matches['cluster_2'].astype(int)
matches['cluster_diff'] = matches['cluster_1'] - matches['cluster_2']

X = matches[['cluster_1', 'cluster_2', 'cluster_diff']]
y = matches['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(class_weight='balanced', solver='liblinear', random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("=== Logistic Regression Report ===")
print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))

print("\nFeature Coefficients:")
for name, coef in zip(X.columns, model.coef_[0]):
    print(f"{name:15}: {coef:.4f}")
