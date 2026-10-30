import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# Setup Tampilan & Style Visualisasi
pd.set_option("display.float_format", lambda x: "%.2f" % x)
sns.set_theme(style="whitegrid")

# ==========================================
# 1. LOAD DATA & DATA CLEANSING
# ==========================================
file_path = "financials_data.xlsx"
df = pd.read_excel(file_path, sheet_name="Sheet1")
df.columns = df.columns.str.strip()

# Penanganan Nilai Kosong pada Discount Band
df["Discount Band"] = df["Discount Band"].fillna("None")

print("=== RINGKASAN DATASET ===")
print(df.info())
print("\nStatistik Deskriptif Utama:")
print(
    df[
        [
            "Units Sold",
            "Manufacturing Price",
            "Sale Price",
            "Sales",
            "COGS",
            "Profit",
        ]
    ].describe()
)

# ==========================================
# 2. FEATURE ENGINEERING
# ==========================================
df["Profit_Margin_Pct"] = (df["Profit"] / df["Sales"]) * 100
df["COGS_Ratio_Pct"] = (df["COGS"] / df["Sales"]) * 100

# ==========================================
# 3. EXPLORATORY DATA ANALYSIS (EDA)
# ==========================================
# Visualisasi 1: Perbandingan Total Sales vs Profit per Segmen
segment_perf = (
    df.groupby("Segment")[["Sales", "Profit"]]
    .sum()
    .sort_values(by="Sales", ascending=False)
    .reset_index()
)
plt.figure(figsize=(9, 4))
sns.barplot(
    data=pd.melt(
        segment_perf, id_vars=["Segment"], value_vars=["Sales", "Profit"]
    ),
    x="Segment",
    y="value",
    hue="variable",
    palette=["#2b5c8f", "#d95f02"],
)
plt.title("Total Sales vs Profit per Segmen Pasar")
plt.ylabel("Total Order ($)")
plt.tight_layout()
plt.savefig('barplot.png')
plt.close()

# Visualisasi 2: Total Profit Berdasarkan Negara dan Produk (Heatmap Pivot)
profit_pivot = df.pivot_table(
    index="Country", columns="Product", values="Profit", aggfunc="sum"
)
plt.figure(figsize=(8, 4))
sns.heatmap(profit_pivot, annot=True, fmt=",.0f", cmap="YlGnBu")
plt.title("Sebaran Total Profit per Negara dan Produk")
plt.tight_layout()
plt.savefig('heatmap.png')
plt.close()

# Visualisasi 3: Efek Discount Band Terhadap Margin Profit (%)
plt.figure(figsize=(8, 4))
sns.boxplot(
    data=df,
    x="Discount Band",
    y="Profit_Margin_Pct",
    palette="Set2",
    order=["None", "Low", "Medium", "High"],
)
plt.title("Distribusi Margin Profit (%) Berdasarkan Tingkat Diskon")
plt.ylabel("Profit Margin (%)")
plt.tight_layout()
plt.savefig('boxplot.png')
plt.close()

# Visualisasi 4: Matriks Korelasi Variabel Keuangan
numeric_cols = [
    "Units Sold",
    "Manufacturing Price",
    "Sale Price",
    "Gross Sales",
    "Discounts",
    "Sales",
    "COGS",
    "Profit",
    "Profit_Margin_Pct",
    "COGS_Ratio_Pct",
]
plt.figure(figsize=(8, 5))
sns.heatmap(df[numeric_cols].corr(), annot=True, fmt=".2f", cmap="Blues")
plt.title("Matriks Korelasi Variabel Keuangan")
plt.tight_layout()
plt.savefig('matrix_corr.png')
plt.close()

# Visualisasi 5: Sensitivitas COGS Ratio vs Profit Margin per Segmen
plt.figure(figsize=(9, 5))
sns.scatterplot(
    data=df,
    x="COGS_Ratio_Pct",
    y="Profit_Margin_Pct",
    hue="Segment",
    style="Segment",
    s=70,
)
plt.title("Analisis Sensitivitas: COGS Ratio (%) vs Profit Margin (%)")
plt.xlabel("COGS Ratio (% dari Sales)")
plt.ylabel("Profit Margin (%)")
plt.tight_layout()
plt.savefig('scatterplot.png')
plt.close()

# ==========================================
# 4. PEMODELAN REGRESI PREDIKSI PROFIT
# ==========================================
X = df[["Units Sold", "Manufacturing Price", "Sale Price", "Discounts", "COGS"]]
y = df["Profit"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("\n=== EVALUASI MODEL REGRESI LINEAR ===")
print(f"R-squared (R2 Score): {r2_score(y_test, y_pred):.4f}")
print(
    f"RMSE: ${np.sqrt(mean_squared_error(y_test, y_pred)):,.2f}"
)

coefficients = pd.DataFrame({"Fitur": X.columns, "Koefisien": model.coef_})
print("\nKoefisien Pengaruh Fitur terhadap Profit:")
print(coefficients)

# ==========================================
# 5. EXPORT HASIL OLAHAN
# ==========================================
df.to_csv("processed_financials.csv", index=False)
print("\n[SELESAI] Data bersih diekspor ke 'processed_financials.csv'")