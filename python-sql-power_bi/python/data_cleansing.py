import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Set format angka desimal agar lebih nyaman dibaca
pd.set_option("display.float_format", lambda x: "%.2f" % x)
sns.set_theme(style="whitegrid")

# 1. Load Data
file_path = "financials_data.xlsx"
df = pd.read_excel(file_path)

# 2. Cleansing Nama Kolom (Menghapus spasi tak terlihat di awal/akhir)
df.columns = df.columns.str.strip()

# 3. Cek Informasi Dasar Data
print("=== INFORMASI DATASET ===")
print(df.info())

print("\n=== 5 BARIS PERTAMA ===")
print(df.head())

print("\n=== STATISTIK DESKRIPTIF ===")
print(
    df[
        [
            "Units Sold",
            "Manufacturing Price",
            "Sale Price",
            "Gross Sales",
            "Discounts",
            "Sales",
            "COGS",
            "Profit",
        ]
    ].describe()
)

print("\n=== CEK NILAI KOSONG (MISSING VALUES) ===")
print(df.isnull().sum())

# 4. Memastikan kolom Date berformat Datetime
df["Date"] = pd.to_datetime(df["Date"])

# 5. Feature Engineering (Membuat Metrik Keuangan Baru)
df["Profit_Margin_Pct"] = (df["Profit"] / df["Sales"]) * 100
df["COGS_Ratio_Pct"] = (df["COGS"] / df["Sales"]) * 100