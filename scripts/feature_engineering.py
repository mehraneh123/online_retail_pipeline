# scripts/feature_engineering.py

import pandas as pd
import numpy as np


class FeatureEngineer:
    """Add new features for analysing"""

    def __init__(self, df):
        self.df = df.copy()
        self.features_added = []

    def create_features(self):
        """Add all features"""
        print("\n" + "=" * 50)
        print("Step4: add new features")
        print("=" * 50)

        self.create_season()
        self.create_transaction_type()
        self.create_customer_segments()
        self.create_product_categories()

        print(f"\n {len(self.features_added)} new features are added:")
        for feature in self.features_added:
            print(f"   - {feature}")

        return self.df

    def create_season(self):
        """Create season based on months"""

        # print("   🔵 create_season is running...")

        if 'Month' in self.df.columns:
            season_map = {
                12: 'Winter', 1: 'Winter', 2: 'Winter',
                3: 'Spring', 4: 'Spring', 5: 'Spring',
                6: 'Summer', 7: 'Summer', 8: 'Summer',
                9: 'Fall', 10: 'Fall', 11: 'Fall'
            }
            self.df['Season'] = self.df['Month'].map(season_map)
            self.features_added.append('Season')

            # print(f"   ✅ Season is made: {self.df['Season'].dropna().unique()}")  # این خط را اضافه کن
        else:
            print("   ❌ Month doesn't exist!")

    def create_transaction_type(self):
        """Transaction type: Sale, Return, Canceled"""
        conditions = []
        categories = []

        if 'IsCancelled' in self.df.columns:
            conditions.append(self.df['IsCancelled'])
            categories.append('Cancelled')

            if 'IsReturn' in self.df.columns:
                # Returns (except for the canceled ones)
                conditions.append(~self.df['IsCancelled'] & self.df['IsReturn'])
                categories.append('Return')

                # Normal Sales
                conditions.append(~self.df['IsCancelled'] & ~self.df['IsReturn'])
                categories.append('Sale')

                self.df['TransactionType'] = np.select(conditions, categories, default='Unknown')
                self.features_added.append('TransactionType')

    def create_customer_segments(self):
        """Identifying customers with repeat purchases (if there is CustomerID)"""
        if 'CustomerID' in self.df.columns:
            # just customer with specific ID
            customer_df = self.df.dropna(subset=['CustomerID'])

            if len(customer_df) > 0:
                # Number of purchases per customer
                customer_counts = customer_df.groupby('CustomerID')['InvoiceNo'].nunique()

                # Loyal customers (with more than 5 purchases)
                loyal_customers = customer_counts[customer_counts > 5].index

                self.df['IsLoyalCustomer'] = False
                self.df.loc[self.df['CustomerID'].isin(loyal_customers), 'IsLoyalCustomer'] = True

                self.features_added.append('IsLoyalCustomer')

                loyal_count = self.df['IsLoyalCustomer'].sum()
                print(f"   - {loyal_count} identified transactions from loyal customers")

    def create_product_categories(self):
        """Product classification by Description"""
        if 'Description' in self.df.columns:
            # simple categorization with keywords
            categories = {
                'BAG': 'Bags',
                'CUSHION': 'Home',
                'LIGHT': 'Home',
                'LANTERN': 'Home',
                'MUG': 'Kitchen',
                'PLATE': 'Kitchen',
                'BOWL': 'Kitchen',
                'GLASS': 'Kitchen',
                'CANDLE': 'Home',
                'HOLDER': 'Home',
                'WRAP': 'Gift',
                'RIBBON': 'Gift',
                'CARD': 'Gift',
                'TOY': 'Toys',
                'DOLL': 'Toys',
                'PAPER': 'Stationery',
                'NOTEBOOK': 'Stationery',
                'PEN': 'Stationery'
            }

            def categorize_product(desc):
                desc_upper = str(desc).upper()
                for keyword, category in categories.items():
                    if keyword in desc_upper:
                        return category
                return 'Other'

            self.df['ProductCategory'] = self.df['Description'].apply(categorize_product)
            self.features_added.append('ProductCategory')