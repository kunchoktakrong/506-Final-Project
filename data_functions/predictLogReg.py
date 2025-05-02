import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

matches = pd.read_csv('../scraping/new_matches.csv')
fighters = pd.read_csv('../scraping/new_fighters.csv')

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
fighters['TDAcc'] = fighters['TDAcc'].apply(convert_pct)
fighters['StrDef'] = fighters['StrDef'].apply(convert_pct)
fighters['TDDef'] = fighters['TDDef'].apply(convert_pct)
fighters['SLpM'] = pd.to_numeric(fighters['SLpM'], errors='coerce')
fighters['TDAvg'] = pd.to_numeric(fighters['TDAvg'], errors='coerce')

fighters = fighters.rename(columns={'name': 'fighter_name'})
matches = matches.merge(fighters, how='left', left_on='fighter_1', right_on='fighter_name').drop(columns='fighter_name')
matches = matches.rename(columns={
    'StrAcc': 'StrAcc_1', 'SLpM': 'SLpM_1', 'TDAvg': 'TDAvg_1',
    'TDAcc': 'TDAcc_1', 'StrDef': 'StrDef_1', 'TDDef': 'TDDef_1'
})
matches = matches.merge(fighters, how='left', left_on='fighter_2', right_on='fighter_name').drop(columns='fighter_name')
matches = matches.rename(columns={
    'StrAcc': 'StrAcc_2', 'SLpM': 'SLpM_2', 'TDAvg': 'TDAvg_2',
    'TDAcc': 'TDAcc_2', 'StrDef': 'StrDef_2', 'TDDef': 'TDDef_2'
})

needed = [
    'StrAcc_1', 'StrAcc_2', 'SLpM_1', 'SLpM_2',
    'TDAvg_1', 'TDAvg_2', 'TDAcc_1', 'TDAcc_2',
    'StrDef_1', 'StrDef_2', 'TDDef_1', 'TDDef_2'
]
matches = matches.dropna(subset=needed)

# Feature differences
matches['StrAcc_diff'] = matches['StrAcc_1'] - matches['StrAcc_2']
matches['SLpM_diff'] = matches['SLpM_1'] - matches['SLpM_2']
matches['TDAvg_diff'] = matches['TDAvg_1'] - matches['TDAvg_2']
matches['TDAcc_diff'] = matches['TDAcc_1'] - matches['TDAcc_2']
matches['StrDef_diff'] = matches['StrDef_1'] - matches['StrDef_2']
matches['TDDef_diff'] = matches['TDDef_1'] - matches['TDDef_2']
matches['label'] = (matches['fighter_1_result'] == 'W').astype(int)

feature_cols = [
    'StrAcc_diff', 'SLpM_diff', 'TDAvg_diff',
    'TDAcc_diff', 'StrDef_diff', 'TDDef_diff'
]
X = matches[feature_cols]
y = matches['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

lr = LogisticRegression(max_iter=1000, class_weight='balanced')
lr.fit(X_train, y_train)
y_pred = lr.predict(X_test)

# Report
print("=== Logistic Regression Report ===")
print(classification_report(y_test, y_pred))

coef_df = pd.DataFrame({
    'Feature': feature_cols,
    'Coefficient': lr.coef_[0]
}).sort_values(by='Coefficient', key=abs, ascending=False)

print("\nFeature Coefficients (sorted by strength):")
print(coef_df)
