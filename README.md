Data Quality Pipeline

A Python-based data quality pipeline for cleaning and validating CSV datasets.

🎯 Project Overview

This project implements a data quality pipeline that:

- Loads data from CSV files

- Performs data quality checks (completeness, consistency, accuracy)

- Cleans data based on defined rules

- Documents all transformations for traceability

🛠️ Technologies Used

- Python 3.14

- Pandas for data manipulation

- NumPy for numerical operations

📁 Project Structure

data-quality-pipeline/
│
├── data/
│ ├── raw/ # Original Kaggle dataset
│ └── cleaned/ # Cleaned output and reports
│
├── scripts/
│ ├── data_loader.py # Data loading module
│ ├── data_validator.py # Data quality checks
│ ├── data_cleaner.py # Data cleaning operations
│ └── main.py # Main pipeline
│
├── docs/
│ └── data_lineage.md # Transformation documentation
│
├── requirements.txt
└── README.md

🚀 How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Download Online Retail - Bojan Tunguz dataset from Kaggle and place it in data/raw/

3. Update the file path in scripts/main.py:

   INPUT_FILE = "data/raw/Online_Retail.csv"

4. Run the pipeline:

   bash

   cd scripts

   python main.py

📊 Output

    Cleaned CSV file in data/cleaned/

    JSON report with validation results

    Data lineage documentation

📝 Example Dataset

This pipeline was tested with Online Retail - Bojan Tunguz dataset from Kaggle, which contains 541,909 rows of Transactions from a UK-based online retail store between 2010-2011.

🔍 Data Quality Checks Performed

Missing value detection

Duplicate removal

Data type validation

Negative value checks

Text standardization

Date format standardization

📈 Results

Original rows: 541,909

Rows after cleaning: 534129

Rows removed: 7780

Total issues identified: 7

📚 What I Learned

Building modular Python scripts

Data validation techniques

Documentation best practices

Working with real-world data quality issues
