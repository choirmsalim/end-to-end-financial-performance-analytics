import pandas as pd
import sqlite3

# Baca data olahan
df = pd.read_csv('processed_financials.csv')

# Simpan ke local database SQLite
conn = sqlite3.connect('FinancialAnalytics.db')
df.to_sql('fact_financials', conn, if_exists='replace', index=False)
conn.close()

print("File FinancialAnalytics.db berhasil dibuat!")