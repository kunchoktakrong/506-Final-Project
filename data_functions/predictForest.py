import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os


def load_data_and_train(test_mode=False):
    base_dir = os.path.dirname(__file__)
    matches = pd.read_csv(os.path.join(base_dir, 'new_matches.csv'))
    clusters = pd.read_csv(os.path.join(base_dir, 'fighter_clusters.csv'))

    matches = matches.merge(clusters.rename(columns={'name': 'fighter_1', 'cluster': 'cluster_1'}), on='fighter_1', how='left')
    matches = matches.merge(clusters.rename(columns={'name': 'fighter_2', 'cluster': 'cluster_2'}), on='fighter_2', how='left')

    matches['label'] = (matches['fighter_1_result'] == 'W').astype(int)
    matches = matches.dropna(subset=['cluster_1', 'cluster_2'])
    matches['cluster_1'] = matches['cluster_1'].astype(int)
    matches['cluster_2'] = matches['cluster_2'].astype(int)
    matches['cluster_diff'] = matches['cluster_1'] - matches['cluster_2']

    X = matches[['cluster_1', 'cluster_2', 'cluster_diff']]
    y = matches['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = RandomForestClassifier(class_weight='balanced', random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    if not test_mode:
        print("=== Random Forest Report ===")
        print(classification_report(y_test, y_pred))

    return model.score(X_test, y_test) 

if __name__ == "__main__":
    load_data_and_train()
