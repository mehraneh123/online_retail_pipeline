# scripts/main.py

import os
import json
from datetime import datetime
from data_loader import DataLoader
from data_validator import DataValidator
from data_cleaner import DataCleaner
from feature_engineering import FeatureEngineer


class OnlineRetailPipeline:
    """Pipeline for Online Retail dataset"""

    def __init__(self, raw_data_path, output_dir='../data'):
        self.raw_data_path = raw_data_path
        self.output_dir = output_dir
        self.df = None
        self.pipeline_log = []

        # Make output folder
        os.makedirs(f"{output_dir}/cleaned", exist_ok=True)
        os.makedirs(f"{output_dir}/reports", exist_ok=True)

    def run(self):
        """Run Pipeline"""
        print("\n" + "★" * 50)
        print(" Start Pipeline check data quality - Online Retail (Kaggle)")
        print("★" * 50)

        start_time = datetime.now()

        # Step1: load data
        loader = DataLoader(self.raw_data_path)
        self.df = loader.load_data()

        if self.df is None:
            print("Error to load data!")
            return

        basic_info = loader.get_basic_info()
        self.pipeline_log.append({'stage': 'load', 'info': basic_info})

        # Step2: check data quality
        validator = DataValidator(self.df)
        issues = validator.run_all_checks()
        validation_summary = validator.get_summary()
        self.pipeline_log.append({'stage': 'validation', 'summary': validation_summary})

        # step3 clean data
        cleaner = DataCleaner(self.df)
        self.df = cleaner.clean()
        cleaning_summary = cleaner.get_cleaning_summary()
        self.pipeline_log.append({'stage': 'cleaning', 'summary': cleaning_summary})

        # Step4: making features
        engineer = FeatureEngineer(self.df)
        self.df = engineer.create_features()
        self.pipeline_log.append({'stage': 'feature_engineering',
                                  'features_added': engineer.features_added})

        # Step5: saving
        self.save_results()

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        print("\n" + "★" * 50)
        print(f"Pipeline is run in {duration:.1f} second")
        print("★" * 50)

        return self.df


    def save_results(self):
        """Save clean data and reports"""
        print("\n" + "=" * 50)
        print("Step5: Save results")
        print("=" * 50)

        # Save CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_path = f"{self.output_dir}/cleaned/online_retail_cleaned_{timestamp}.csv"
        self.df.to_csv(csv_path, index=False)
        print(f"Cleaned data: {csv_path}")

        # Save a small sample for testing
        sample_path = f"{self.output_dir}/cleaned/online_retail_sample.csv"
        self.df.head(1000).to_csv(sample_path, index=False)
        print(f"Sample 1000 records : {sample_path}")

        # Save Report JSON
        report = {
            'pipeline_execution': {
                'timestamp': datetime.now().isoformat(),
                'dataset': 'Online Retail (Kaggle)',
                'duration_seconds': (datetime.now() - start_time).total_seconds()
            },
            'logs': self.pipeline_log,
            'final_shape': list(self.df.shape),
            'columns': list(self.df.columns)
        }

        report_path = f"{self.output_dir}/reports/pipeline_report_{timestamp}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)

        print(f"Report JSON: {report_path}")

        # Last Statistics
        print(f"\n The final statistics dataset:")
        print(f"   - count rows: {len(self.df):,}")
        print(f"   - count columns: {len(self.df.columns)}")
        print(f"   - new columns: {list(self.df.columns)[8:]}")  # added columns


# Save start time for using in save_results
start_time = datetime.now()

if __name__ == "__main__":
    # Adjust the rout of the dataset
    # Download the dataset from Kaggle and put it in data/raw
    RAW_DATA_PATH = "../data/raw/online_retail.csv"  # Name the dataset

    pipeline = OnlineRetailPipeline(RAW_DATA_PATH)
    pipeline.run()




