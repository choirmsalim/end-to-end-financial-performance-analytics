-- ============================================================================
-- 1. PEMBERSIHAN SKEMA 
-- ============================================================================
DROP VIEW IF EXISTS vw_financial_kpi_summary;
DROP TABLE IF EXISTS fact_financial_transactions;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_geography;
DROP TABLE IF EXISTS dim_segment;

-- ============================================================================
-- 2. PEMBUATAN SKEMA STAR SCHEMA
-- ============================================================================
CREATE TABLE dim_product (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT UNIQUE,
    manufacturing_price REAL
);

CREATE TABLE dim_geography (
    geography_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_name TEXT UNIQUE
);

CREATE TABLE dim_segment (
    segment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    segment_name TEXT UNIQUE
);

CREATE TABLE fact_financial_transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    geography_id INTEGER,
    segment_id INTEGER,
    date TEXT,
    year INTEGER,
    month_number INTEGER,
    units_sold REAL,
    sale_price REAL,
    gross_sales REAL,
    discounts REAL,
    sales REAL,
    cogs REAL,
    profit REAL,
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY (geography_id) REFERENCES dim_geography(geography_id),
    FOREIGN KEY (segment_id) REFERENCES dim_segment(segment_id)
);

-- ============================================================================
-- 3. INISIALISASI DATA DIMENSI
-- ============================================================================
INSERT OR IGNORE INTO dim_product (product_name, manufacturing_price)
SELECT DISTINCT Product, Manufacturing_Price FROM fact_financials;

INSERT OR IGNORE INTO dim_geography (country_name)
SELECT DISTINCT Country FROM fact_financials;

INSERT OR IGNORE INTO dim_segment (segment_name)
SELECT DISTINCT Segment FROM fact_financials;

-- ============================================================================
-- 4. POPULASI TABEL (ETL MAPPING)
-- ============================================================================
INSERT INTO fact_financial_transactions (
    product_id, geography_id, segment_id, date, year, month_number,
    units_sold, sale_price, gross_sales, discounts, sales, cogs, profit
)
SELECT 
    p.product_id,
    g.geography_id,
    s.segment_id,
    f.Date,
    f.Year,
    f.Month_Number,
    f.Units_Sold,
    f.Sale_Price,
    f.Gross_Sales,
    f.Discounts,
    f.Sales,
    f.COGS,
    f.Profit
FROM fact_financials f
JOIN dim_product p ON f.Product = p.product_name
JOIN dim_geography g ON f.Country = g.country_name
JOIN dim_segment s ON f.Segment = s.segment_name;

-- ============================================================================
-- 5. KUERI KPI 1: PROFIT MARGIN RATIO PER SEGMEN & NEGARA
-- ============================================================================
SELECT 
    s.segment_name AS Segment,
    g.country_name AS Country,
    ROUND(SUM(f.sales), 2) AS Total_Sales,
    ROUND(SUM(f.profit), 2) AS Total_Profit,
    ROUND((SUM(f.profit) / SUM(f.sales)) * 100, 2) AS Profit_Margin_Pct
FROM fact_financial_transactions f
JOIN dim_segment s ON f.segment_id = s.segment_id
JOIN dim_geography g ON f.geography_id = g.geography_id
GROUP BY s.segment_name, g.country_name
ORDER BY Profit_Margin_Pct DESC;

-- ============================================================================
-- 6. KUERI KPI 2: COGS TO SALES RATIO (EFISIENSI BIAYA PRODUKSI)
-- ============================================================================
SELECT 
    p.product_name AS Product,
    ROUND(SUM(f.sales), 2) AS Total_Sales,
    ROUND(SUM(f.cogs), 2) AS Total_COGS,
    ROUND((SUM(f.cogs) / SUM(f.sales)) * 100, 2) AS COGS_to_Sales_Ratio_Pct
FROM fact_financial_transactions f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.product_name
ORDER BY COGS_to_Sales_Ratio_Pct ASC;

-- ============================================================================
-- 7. KUERI KPI 3: YEAR-OVER-YEAR (YoY) GROWTH (2013 VS 2014)
-- ============================================================================
WITH YearlySales AS (
    SELECT 
        year,
        SUM(sales) AS total_sales
    FROM fact_financial_transactions
    WHERE year IN (2013, 2014)
    GROUP BY year
),
YoYCalculation AS (
    SELECT 
        year,
        total_sales,
        LAG(total_sales) OVER (ORDER BY year) AS prev_year_sales
    FROM YearlySales
)
SELECT 
    year AS Year,
    ROUND(total_sales, 2) AS Current_Year_Sales,
    ROUND(prev_year_sales, 2) AS Previous_Year_Sales,
    ROUND(((total_sales - prev_year_sales) / prev_year_sales) * 100, 2) AS YoY_Growth_Pct
FROM YoYCalculation
WHERE prev_year_sales IS NOT NULL;

-- ============================================================================
-- 8. PEMBUATAN VIEW ANALITIS & INDEKSASI
-- ============================================================================
CREATE VIEW vw_financial_kpi_summary AS
SELECT 
    f.transaction_id,
    f.date,
    f.year,
    s.segment_name AS Segment,
    g.country_name AS Country,
    p.product_name AS Product,
    f.units_sold,
    f.sales,
    f.cogs,
    f.profit,
    ROUND((f.profit / f.sales) * 100, 2) AS Profit_Margin_Pct,
    ROUND((f.cogs / f.sales) * 100, 2) AS COGS_Ratio_Pct
FROM fact_financial_transactions f
JOIN dim_segment s ON f.segment_id = s.segment_id
JOIN dim_geography g ON f.geography_id = g.geography_id
JOIN dim_product p ON f.product_id = p.product_id;

CREATE INDEX IF NOT EXISTS idx_fact_year ON fact_financial_transactions(year);
CREATE INDEX IF NOT EXISTS idx_fact_product ON fact_financial_transactions(product_id);
CREATE INDEX IF NOT EXISTS idx_fact_geography ON fact_financial_transactions(geography_id);
CREATE INDEX IF NOT EXISTS idx_fact_segment ON fact_financial_transactions(segment_id);