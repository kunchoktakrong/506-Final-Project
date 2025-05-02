import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

matches = pd.read_csv('../scraping/new_matches.csv')

matches = matches.rename(columns={matches.columns[12]: "sig_str_pct_1"})

def convert_percentage(x):
    if isinstance(x, str):
        try:
            return float(x.replace('%', '').strip())
        except Exception as e:
            print(f"Error converting {x}: {e}")
            return None
    return x

matches['sig_str_pct_1'] = matches['sig_str_pct_1'].apply(convert_percentage)
matches['sig_str_pct_2'] = matches['sig_str_pct_2'].apply(convert_percentage)

matches_clean = matches.dropna(subset=['sig_str_pct_1', 'sig_str_pct_2'])

matches_clean = matches_clean[
    (matches_clean['sig_str_pct_1'] != 0) &
    (matches_clean['sig_str_pct_1'] != 100) &
    (matches_clean['sig_str_pct_2'] != 0) &
    (matches_clean['sig_str_pct_2'] != 100)
]

plt.figure(figsize=(8, 6))
sns.scatterplot(data=matches_clean, x='sig_str_pct_1', y='sig_str_pct_2', s=100, alpha=0.7)
plt.xlabel("Fighter 1 Significant Strike %")
plt.ylabel("Fighter 2 Significant Strike %")
plt.title("Fighter 1 vs. Fighter 2 Significant Strike Percentage (Ignoring 0's and 100's)")
plt.grid(True)
plt.show()
