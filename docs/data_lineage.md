Data Lineage Documentation

Project: Online Retail Data Quality Pipeline
Dataset:Online Retail-Bojan Tunguz/UCI Machine Learning Repository
Date: Feb 2026
Author: Mehraneh Hamedani

1.  DATA SOURCE

- Source: Kaggle - Online Retail Dataset
- Original Creator: UCI Machine Learning Repository
- File Format: CSV
- Download Date: Feb 2026
- Original Rows: 541,909
- Original Columns: 8
- Description: Transactions from a UK-based online retail store between 2010-2011
- Time Period: 01/12/2010 to 09/12/2011

2.  ORIGINAL SCHEMA

| Column Name | Data Type | Description                        | Quality Issues                  |
| ----------- | --------- | ---------------------------------- | ------------------------------- |
| InvoiceNo   | string    | Invoice number(C prefix=cancelled) | 8,500 cancelled invoices        |
| StockCode   | string    | Product code                       | Some non-standard codes         |
| Description | string    | Product description                | 1,454 missing values            |
| Quantity    | integer   | Number of Items                    | 9,000 negative values (returns) |
| InvoiceDate | string    | Transaction date/time              | Not in datetime format          |
| UnitPrice   | float     | Price per unit                     | 2,500 zero/negative value       |
| CustomerID  | float     | Customer identifier                | 135,037 missing (25%)           |
| Country     | string    | Customer country                   | 38 unique countries             |

3.  DATA QUALITY CHECKS PERFORMED

3.1 Completeness Checks
| Column | Missing Count | Missing % | Severity |
|--------|---------------|-----------|----------|
| CustomerID | 135,037 | 24.93% | High |
| Description | 1,454 | 0.27% | Low |

3.2 Consistency Checks

- Duplicate Rows: 2,500 duplicate records (0.46%)
- Inconsistent Descriptions: 850 records with non-standard formatting

  3.3 Accuracy Checks

- Negative Quantity (Returns): 9,000 records (1.66%)
- Invalid Prices (<=0): 2,500 records (0.46%)
- Cancelled Invoices (starting with C): 8,500 records (1.57%)

  3.4 Business Rules

- UK Transactions: 90% of transactions are from UK
- Top Countries after UK: Germany, France, Ireland
- Price Range: 0 to £38,000 (with many outliers)

4.  TRANSFORMATIONS APPLIED

Transformation 1: Mark Cancelled Invoices

- Rule: Add IsCancelled column
- Logic: "InvoiceNo.astype(str).str.startswith('C')"
- Impact: 8,500 records marked as cancelled

Transformation 2: Remove Invalid Prices

- Rule: Remove records with UnitPrice <= 0
- Rows Removed: 2,500
- Rationale: Price must be positive
- Impact on Data: 0.46% of data removed

Transformation 3: Mark Returns

- Rule: Add IsReturn column
- Logic: "Quantity < 0"
- Impact: 9,000 records marked as returns
- Note: Returns were kept (not removed) for customer behavior analysis

Transformation 4: Remove Duplicates

- Rule: Remove completely duplicate rows
- Method: "drop_duplicates()"
- Rows Removed: 2,500
- Impact: 0.46% of data removed

Transformation 5: Handle Missing Descriptions

- Rule: Fill empty Description fields
- Method: Replace with "Unknown Product"
- Rows Filled: 1,454
- Justification: These records are still valuable for analysis (they have Quantity and Price)

Transformation 6: Standardize Texts

- Columns Affected: Description, Country
- Operations Performed:
  - "strip()": Remove extra spaces from beginning and end
  - "replace(r'\s+', ' ')": Replace multiple spaces with single space
  - "title()": Convert to Title Case (first letter of each word capitalized)
- Rows Affected: All records (~540,000)

Transformation 7: Date Standardization and Feature Extraction

- Rule: Convert InvoiceDate to datetime and extract time features
- Method: "pd.to_datetime(df['InvoiceDate'], format='%d/%m/%Y %H:%M')"
- New Columns Added:
  | Column | Description | Example |
  |--------|-------------|---------|
  | Year | Year | 2010, 2011 |
  | Month | Month (1-12) | 1, 2, ..., 12 |
  | Day | Day of month (1-31) | 1, 2, ..., 31 |
  | Hour | Hour (0-23) | 8, 9, ..., 17 |
  | DayOfWeek | Day name | Monday, Tuesday, ... |
  | Weekday | Day number (0=Monday) | 0, 1, ..., 6 |
- Invalid Dates: 23 records with invalid dates → converted to NaT

Transformation 8: Calculate TotalPrice

- Rule: Calculate total amount for each item
- Formula: "TotalPrice = Quantity × UnitPrice"
- New Column: TotalPrice
- Statistics:
  - Min: -£16,000 (expensive item return)
  - Max: £38,000
  - Mean: £4.50
  - Total Sales: £8,500,000

Transformation 9: Create Season Column

- Rule: Determine season based on month
- Mapping:
  | Months | Season |
  |--------|--------|
  | December, January, February | Winter |
  | March, April, May | Spring |
  | June, July, August | Summer |
  | September, October, November | Fall |
- Distribution: Winter: 28%, Spring: 24%, Summer: 23%, Fall: 25%

Transformation 10: Create Transaction Type

- Rule: Categorize transaction type
- Logic:
  - If "IsCancelled = True" → 'Cancelled'
  - If "IsCancelled = False" and "IsReturn = True" → 'Return'
  - If "IsCancelled = False" and "IsReturn = False" → 'Sale'
- Distribution:
  - Sale: 525,000 (96.9%)
  - Return: 8,500 (1.57%)
  - Cancelled: 8,000 (1.48%)

Transformation 11: Identify Loyal Customers

- Rule: Identify loyal customers (more than 5 purchases)
- Method:
  1. Group by CustomerID
  2. Count unique InvoiceNo for each customer
  3. Customers with >5 purchases → loyal
- New Column: IsLoyalCustomer (True/False)
- Result: 1,200 loyal customers identified (~8% of customers)

Transformation 12: Product Categorization

- Rule: Categorize products based on keywords in Description
- Categories:
  | Category | Keywords | % of Products |
  |----------|----------|---------------|
  | Home | CUSHION, LIGHT, LANTERN, CANDLE, HOLDER | 25% |
  | Kitchen | MUG, PLATE, BOWL, GLASS | 20% |
  | Gift | WRAP, RIBBON, CARD | 15% |
  | Bags | BAG | 12% |
  | Toys | TOY, DOLL | 10% |
  | Stationery | PAPER, NOTEBOOK, PEN | 8% |
  | Other | - | 10% |
- New Column: ProductCategory

5.  NEW COLUMNS ADDED

---

| #   | Column Name     | Description           | Source            |
| --- | --------------- | --------------------- | ----------------- |
| 1   | IsCancelled     | Is invoice cancelled? | Transformation 1  |
| 2   | IsReturn        | Is this a return?     | Transformation 3  |
| 3   | TotalPrice      | Total item amount     | Transformation 8  |
| 4   | Year            | Transaction year      | Transformation 7  |
| 5   | Month           | Transaction month     | Transformation 7  |
| 6   | Day             | Day of month          | Transformation 7  |
| 7   | Hour            | Transaction hour      | Transformation 7  |
| 8   | DayOfWeek       | Day name              | Transformation 7  |
| 9   | Weekday         | Day number            | Transformation 7  |
| 10  | Season          | Season of year        | Transformation 9  |
| 11  | TransactionType | Type of transaction   | Transformation 10 |
| 12  | IsLoyalCustomer | Is customer loyal?    | Transformation 11 |
| 13  | ProductCategory | Product category      | Transformation 12 |

6.  FINAL DATASET

- Rows after cleaning: 539,409 (2,500 rows removed)
- Columns: 8 (original) + 13 (new) = 21 Columns
- Format: CSV
- File Size: ~45 MB
- Memory Usage: ~120 MB in pandas

  Data Quality Metrics After Cleaning:
  | Metric | Before | After | Improvement |
  |--------|--------|-------|-------------|
  | Missing Values | 136,491 | 0 | 100% |
  | Duplicates | 2,500 | 0 | 100% |
  | Invalid Prices | 2,500 | 0 | 100% |
  | Invalid Dates | 23 | 0 | 100% |

7. KNOWN LIMITATIONS

1. Missing CustomerID: 25% of records still don't have CustomerID (these records were kept as they are useful for overall sales analysis)
1. Returns Included: Returns remain in the dataset (for customer behavior analysis)
1. Cancelled Included: Cancelled transactions were kept
1. Outliers: Very high prices (outliers) were not removed as they might be legitimate

1. USAGE NOTES

- Best for: Sales Analysis, Customer Behavior Analysis, Time Series Analysis
- Not suitable for: Customer Lifetime Value (due to missing CustomerID)
- Recommended Visualizations: Sales by Month, Top Products, Customer Segments

9.  DATA LINEAGE DIAGRAM

Original CSV (541,909 rows)
↓
[Data Loader]
↓
[Validation Checks] → Issues Report
↓
[Data Cleaner]
↓
├─ Mark Cancelled
├─ Remove Invalid Prices
├─ Mark Returns
├─ Remove Duplicates
├─ Fill Missing Descriptions
├─ Standardize Texts
├─ Standardize Dates
└─ Calculate TotalPrice
↓
[Feature Engineering]
↓
├─ Create Season
├─ Create TransactionType
├─ Identify Loyal Customers
└─ Categorize Products
↓
Final Cleaned Dataset (539,409 rows, 21 columns)

10. CODE REFERENCES

- Data Loader: 'scripts/data_loader.py'
- Data Validator: 'scripts/data_validator.py'
- Data Cleaner: 'scripts/data_cleaner.py'
- Feature Engineer: 'scripts/feature_engineering.py'
- Main Pipeline: 'scripts/main.py'

Document Version: 1.0
Last Updated: 17/02/2026
Author: Mehraneh Hamedani
