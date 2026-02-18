# scripts/data_loader.py

import pandas as pd
import os
from datetime import datetime


class DataLoader:
    """Load dataset Online Retail from Kaggle"""

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.loading_report = {}

    def load_data(self):
        """Load CSV with appropriate encoding"""
        print("=" * 50)
        print("Step1: load data")
        print("=" * 50)

        try:
            # Dataset Online Retail with latin encoding
            self.df = pd.read_csv(self.file_path, encoding='ISO-8859-1')
            print(f"Load the file with successfully")
            print(f"   count rows: {len(self.df):,}")
            print(f"   count columns: {len(self.df.columns)}")
            print(f"   columns: {list(self.df.columns)}")

            return self.df

        except Exception as e:
            print(f"Error in loading the file: {e}")
            return None

    def get_basic_info(self):
        """Basic information of dataset"""
        if self.df is None:
            return None

        info = {
            'shape': [int(self.df.shape[0]), int(self.df.shape[1])],  # int for JSON
            'columns': list(self.df.columns),
            'data_types': {col: str(dtype) for col, dtype in self.df.dtypes.items()},
            'missing_values': {col: int(val) for col, val in self.df.isnull().sum().items()},
            'duplicates': int(self.df.duplicated().sum()),
            'memory_usage_mb': round(self.df.memory_usage().sum() / 1024 ** 2, 2)
        }

        print("\ninitial statistics of dataset")
        print(f"   - usage memory: {info['memory_usage_mb']} MB")
        print(f"   - duplicated records: {info['duplicates']:,}")

        # Missing columns
        missing_cols = {col: val for col, val in info['missing_values'].items() if val > 0}
        if missing_cols:
            print(f"   - missing columns: {len(missing_cols)}")
            for col, val in missing_cols.items():
                percent = (val / info['shape'][0]) * 100
                print(f"     * {col}: {val:,} ({percent:.1f}%)")

        self.loading_report = info
        return info