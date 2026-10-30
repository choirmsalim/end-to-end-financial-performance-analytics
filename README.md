# end-to-end-financial-performance-analytics
"An end-to-end financial analytics project featuring an Python EDA &amp; Linear Regression, SQL Data Mart (Star Schema), What-If Business Simulation in Excel, and an executive Power BI Sales Performance Dashboard."


# H+ Financial Analytics: End-to-End Data Project

Analisis end-to-end atas 700 transaksi penjualan perusahaan fiktif **H+** (Sep 2013 – Des 2014): dari data cleansing dan modeling di **Python**, KPI di **SQL**, simulasi skenario di **Excel**, sampai dashboard eksekutif di **Power BI**.

![Dashboard Preview](images/dashboard_preview.png)

---

## 1. Overview

**Tujuan:** menemukan sumber profit dan kerugian, serta mengukur pengaruh **diskon** dan **COGS** terhadap profitabilitas.

**Pertanyaan bisnis yang dijawab:**

| Alat | Pertanyaan |
|---|---|
| Python | Segmen, produk, dan negara mana yang paling menguntungkan? Mengapa ada transaksi rugi? Seberapa besar dampak diskon? Faktor apa yang memengaruhi profit? |
| SQL | Berapa profit margin per segmen/negara, rasio COGS per produk, dan pertumbuhan YoY? |
| Excel | Seberapa sensitif profit terhadap kenaikan COGS dan pemotongan diskon? |
| Power BI | Bagaimana eksekutif memantau penjualan, biaya, dan profit dalam satu halaman? |

**Hasil utama:**

| Total Sales | Total Profit | Profit Margin | Diskon | COGS |
|---|---|---|---|---|
| **$118.7M** | **$16.9M** | **14.23%** | $9.2M | $101.8M |

---

## 2. Dataset

- **File:** `financials_data.xlsx` (Sheet1), 700 baris
- **Periode:** September 2013 – Desember 2014

| Kelompok | Kolom |
|---|---|
| Dimensi | Segment (5), Country (5), Product (6), Discount Band (None/Low/Medium/High) |
| Metrik | Units Sold, Manufacturing Price, Sale Price, Gross Sales, Discounts, Sales, COGS, Profit |
| Waktu | Date, Month Number, Month Name, Year |
| Fitur turunan | `Profit_Margin_Pct` = Profit / Sales, `COGS_Ratio_Pct` = COGS / Sales |

**Segmen:** Government, Small Business, Enterprise, Midmarket, Channel Partners
**Negara:** United States of America, Canada, France, Germany, Mexico
**Produk:** Paseo, VTT, Amarilla, Velo, Montana, Carretera

---

## 3. Tools

| Kategori | Tools |
|---|---|
| Analisis & modeling | Python (Pandas, NumPy, Matplotlib, Seaborn, Scikit-Learn) |
| Database & KPI | SQL (MySQL, star schema, window function) |
| Business insight | Microsoft Excel (PivotTable, Scenario Manager, Data Table) |
| Visualisasi | Power BI Desktop |
| Version control | Git & GitHub |

---

## 4. Langkah Pengerjaan

1. **Data cleansing (`python/data_cleansing.py`)**: merapikan spasi nama kolom, mengisi `Discount Band` kosong dengan `None`, mengonversi `Date` ke datetime, dan membuat fitur margin serta COGS ratio.
2. **EDA & modeling (`python/eda_and_modeling.py`)**: 5 visualisasi (barplot, heatmap, boxplot, matriks korelasi, scatterplot) dan regresi linear untuk prediksi Profit (split 80/20), lalu mengekspor `processed_financials.csv`.
3. **SQL (`sql/financial_analysis_queries.sql`)**: membangun star schema (1 tabel fakta + 3 dimensi), 3 kueri KPI, serta view `vw_financial_kpi_summary` untuk Power BI.
4. **Excel (`excel/`)**: P&L pivot per negara × produk, Scenario Manager, dan Data Table dua variabel (perubahan COGS × pemotongan diskon).
5. **Power BI (`powerbi/`)**: dashboard interaktif dengan KPI, tren bulanan, waterfall Gross Sales → Profit, dan profit per segmen.
6. **Report & presentasi (`reports/`)**: laporan end-to-end dan deck ringkasan untuk stakeholder.

---

## 5. Hasil & Insight

### Python: EDA & Modeling

- **Government** ($52.5M) dan **Small Business** ($42.4M) adalah segmen penjualan terbesar. Profit Government $11.4M, Small Business $4.1M.
- **Enterprise** menjual $19.6M tetapi **merugi** (profit -$0.6M, margin -3.13%) karena COGS Ratio melampaui 100% pada sebagian transaksi (58 dari 700 transaksi rugi).
- **Channel Partners** punya margin tertinggi (**73.1%**) walau volumenya kecil ($1.8M).
- **Paseo** adalah produk utama: profit terbesar di hampir semua negara (Canada $1.27M, USA $1.02M, Mexico $0.93M).
- **Diskon menekan margin:** median margin turun dari ±33% (tanpa diskon) menjadi ±19% (High). Margin negatif hanya muncul di band Medium dan High.
- **Korelasi:** Sales–COGS 0.99, Sales–Profit 0.81, Sale Price–Profit 0.65.
- **Model regresi linear:** R² **0.64**, RMSE **$27.6K**. Sale Price adalah faktor paling berpengaruh, sedangkan diskon menurunkan profit. *Catatan: COGS, Discounts, dan Sale Price saling berkorelasi, sehingga koefisien perlu dibaca hati-hati.*

| | | |
|---|---|---|
| ![Barplot](images/barplot.png) | ![Heatmap](images/heatmap.png) | ![Boxplot](images/boxplot.png) |
| ![Korelasi](images/matrix_corr.png) | ![Scatter](images/scatterplot.png) | |

### SQL: KPI

| KPI | Temuan |
|---|---|
| Profit Margin per Segmen–Negara | Channel Partners menempati margin tertinggi di semua negara (±73%); Enterprise terendah |
| COGS-to-Sales per Produk | Terbaik **Amarilla (84.1%)**, terburuk **Velo (87.4%)**; Paseo 85.5% |
| YoY Growth 2013 → 2014 | $26.4M → $92.3M (**+249%**). *Catatan: data 2013 hanya 4 bulan (Sep–Des)* |

### Excel: What-If Analysis

- Setiap **+1% COGS** menurunkan profit sekitar **$1.02M**.
- Setiap **pemangkasan diskon 25%** menambah profit sekitar **$2.3M** (dengan asumsi volume penjualan tetap).
- Profit jauh lebih sensitif terhadap COGS daripada terhadap diskon.

### Power BI: Dashboard

- Penjualan memuncak pada Oktober–Desember (Okt 2014 $12.4M, Des 2014 $12.0M).
- COGS menyerap **79.6%** dari Gross Sales ($127.9M).
- Volume tinggi tidak selalu berarti profit tinggi.

---

## 6. Rekomendasi Bisnis

1. **Restrukturisasi Enterprise:** naikkan harga, tetapkan price floor, dan hentikan transaksi di bawah break-even.
2. **Disiplinkan diskon:** batasi High Discount Band dan terapkan persetujuan berjenjang.
3. **Prioritaskan Paseo** di Canada dan USA sebagai penggerak profit.
4. **Tekan COGS:** negosiasi pemasok untuk produk dengan rasio COGS tertinggi (Velo, Carretera).
5. **Kembangkan Channel Partners dan Midmarket** yang bermargin tinggi namun masih kecil.
6. **Siapkan stok dan kapasitas** menjelang puncak penjualan Oktober–Desember.

---

## 7. Struktur Repository

```
hplus-financial-analytics/
├── data/
│   ├── financials_data.xlsx
│   └── processed_financials.csv
├── python/
│   ├── data_cleansing.py
│   └── eda_and_modeling.py
├── sql/
│   └── financial_analysis_queries.sql
├── excel/
│   └── executive-financial-whatif-analysis.xlsx
├── powerbi/
│   └── H+_Sales_Dashboard.pbix
├── images/               # grafik EDA & preview dashboard
├── reports/
│   ├── end-to-end-project-report.pdf
│   └── presentation.pptx
└── README.md
```

---

## 8. How to Run

### Prasyarat
- Python 3.9+
- Power BI Desktop (untuk membuka `.pbix`)
- Microsoft Excel (untuk membuka workbook What-If Analysis)
- MySQL 

### a. Clone & instal dependensi

```bash
git clone https://github.com/<username>/hplus-financial-analytics.git
cd hplus-financial-analytics
pip install pandas numpy matplotlib seaborn scikit-learn openpyxl
```

### b. Jalankan analisis Python

Letakkan `financials_data.xlsx` di folder yang sama dengan skrip, lalu:

```bash
cd python
python data_cleansing.py        # cek kualitas data & feature engineering
python eda_and_modeling.py      # grafik EDA, model regresi, export processed_financials.csv
```

### c. Jalankan SQL 

Skrip SQL membaca tabel staging `fact_financials`. Muat dulu data bersih ke SQLite:

```python
import sqlite3, pandas as pd

df = pd.read_csv("processed_financials.csv")
df.columns = df.columns.str.replace(" ", "_")   # Units Sold -> Units_Sold, dst.

conn = sqlite3.connect("FinancialAnalytics.db")
df.to_sql("fact_financials", conn, if_exists="replace", index=False)
conn.close()
```

Lalu eksekusi skrip (membuat star schema, KPI, dan view):

```bash
sqlite3 FinancialAnalytics.db < sql/financial_analysis_queries.sql
```

### d. Excel dan Power BI

- **Excel:** buka `excel/executive-financial-whatif-analysis.xlsx`. Ubah sel *Perubahan COGS* dan *Pemotongan Discount* pada sheet `DataTable_WhatIfAnalysis`, atau lihat sheet `ScenarioSummary`.
- **Power BI:** buka `powerbi/H+_Sales_Dashboard.pbix`, lalu *Refresh* setelah mengarahkan sumber data ke `processed_financials.csv` atau view `vw_financial_kpi_summary`.


> Dataset bersifat fiktif dan digunakan untuk tujuan pembelajaran dan portofolio.
