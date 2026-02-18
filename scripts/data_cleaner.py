# scripts/data_cleaner.py

import pandas as pd
from datetime import datetime


class DataCleaner:
    """Clean data for dataset Online Retail"""

    def __init__(self, df):
        self.df = df.copy()
        self.cleaning_log = []
        self.transformation_rules = []
        self.stats_before = {'rows': len(df)}

    def clean(self):
        """Run all cleaning steps"""
        print("\n" + "=" * 50)
        print("Step3: clean data")
        print("=" * 50)

        # delete cancelled invoices (optional - keep them but in a separate)
        self.separate_cancelled()

        # مStep2: delete records with invalid price
        self.remove_invalid_prices()

        # Step3: manage Quantity negative (keep returns in a separate)
        self.mark_returns()

        # Step4: delete duplicated records
        self.remove_duplicates()

        # Step5: manage null values in Description
        self.handle_missing_descriptions()

        # Step6: standardize texts
        self.standardize_texts()

        # Step7: standardize dates
        self.standardize_dates()

        # Step8: add column TotalPrice
        self.calculate_total_price()

        print(f"\nFinal statistics:")
        print(f"   - Initial records: {self.stats_before['rows']:,}")
        print(f"   - Final records: {len(self.df):,}")
        print(f"   - Deleted records: {self.stats_before['rows'] - len(self.df):,}")
        print(f"   - Count transformations: {len(self.transformation_rules)}")

        return self.df

    def separate_cancelled(self):
        """Separate canceled invoices (not deleted, just marked)"""
        initial_count = len(self.df)

        if 'InvoiceNo' in self.df.columns:
            # Add new column to show cancel
            self.df['IsCancelled'] = self.df['InvoiceNo'].astype(str).str.startswith('C')
            cancelled_count = self.df['IsCancelled'].sum()

            self.transformation_rules.append({
                'rule': 'Mark cancelled invoices',
                'description': f"Added IsCancelled column, {cancelled_count} cancelled invoices"
            })

            self.cleaning_log.append({
                'step': 'separate_cancelled',
                'cancelled_found': int(cancelled_count)
            })

            print(f"   - {cancelled_count} Cancelled invoices identified and marked")

    def remove_invalid_prices(self):
        """Delete records with invalid price (zero or negative)"""
        initial_count = len(self.df)

        if 'UnitPrice' in self.df.columns:
            self.df = self.df[self.df['UnitPrice'] > 0]
            removed = initial_count - len(self.df)

            if removed > 0:
                self.transformation_rules.append({
                    'rule': 'Remove invalid prices',
                    'rows_removed': int(removed)
                })

                self.cleaning_log.append({
                    'step': 'remove_invalid_prices',
                    'rows_removed': int(removed)
                })

                print(f"   - {removed} deleted record with invalid price")

    def mark_returns(self):
        """Marked returnsا (Quantity negative)"""
        if 'Quantity' in self.df.columns:
            self.df['IsReturn'] = self.df['Quantity'] < 0
            returns_count = self.df['IsReturn'].sum()

            self.transformation_rules.append({
                'rule': 'Mark returns',
                'description': f"Added IsReturn column, {returns_count} returns"
            })

            self.cleaning_log.append({
                'step': 'mark_returns',
                'returns_found': int(returns_count)
            })

            print(f"   - {returns_count} returned product identified and marked")

    def remove_duplicates(self):
        """Deleted duplicated records"""
        initial_count = len(self.df)

        self.df = self.df.drop_duplicates()
        removed = initial_count - len(self.df)

        if removed > 0:
            self.transformation_rules.append({
                'rule': 'Remove duplicates',
                'rows_removed': int(removed)
            })

            self.cleaning_log.append({
                'step': 'remove_duplicates',
                'rows_removed': int(removed)
            })

            print(f"   - {removed} deleted duplicated record")

    def handle_missing_descriptions(self):
        """Manage null in Description"""
        if 'Description' in self.df.columns:
            missing_desc = self.df['Description'].isnull().sum()

            if missing_desc > 0:
                # Fill it with "Unknown Product"
                self.df.loc[self.df['Description'].isnull(), 'Description'] = 'Unknown Product'

                self.transformation_rules.append({
                    'rule': 'Fill missing descriptions',
                    'rows_filled': int(missing_desc)
                })

                self.cleaning_log.append({
                    'step': 'handle_missing_descriptions',
                    'rows_filled': int(missing_desc)
                })

                print(f"   - {missing_desc} Fill null description with 'Unknown Product'")

    def standardize_texts(self):
        """Standardize texts"""
        changes = 0

        if 'Description' in self.df.columns:
            # Removing extra spaces and standardizing
            original = self.df['Description'].copy()
            self.df['Description'] = self.df['Description'].astype(str).str.strip()
            self.df['Description'] = self.df['Description'].str.replace(r'\s+', ' ', regex=True)
            self.df['Description'] = self.df['Description'].str.title()  # capital initial letter

            changes += (original != self.df['Description']).sum()

        if 'Country' in self.df.columns:
            original = self.df['Country'].copy()
            self.df['Country'] = self.df['Country'].astype(str).str.strip()
            self.df['Country'] = self.df['Country'].str.title()

            changes += (original != self.df['Country']).sum()

        if changes > 0:
            self.transformation_rules.append({
                'rule': 'Standardize texts',
                'rows_affected': int(changes)
            })

            self.cleaning_log.append({
                'step': 'standardize_texts',
                'rows_affected': int(changes)
            })

            print(f"   - {changes} standardized text records")

    def standardize_dates(self):
        """Standardize text column"""
        if 'InvoiceDate' in self.df.columns:
            try:
                # Change to datetime
                self.df['InvoiceDate'] = pd.to_datetime(
                    self.df['InvoiceDate'],
                    infer_datetime_format=True,  # Tried to identify format
                    errors='coerce'
                )

                # Extract time features
                self.df['Year'] = self.df['InvoiceDate'].dt.year
                self.df['Month'] = self.df['InvoiceDate'].dt.month
                self.df['Day'] = self.df['InvoiceDate'].dt.day
                self.df['Hour'] = self.df['InvoiceDate'].dt.hour
                self.df['DayOfWeek'] = self.df['InvoiceDate'].dt.day_name()
                self.df['Weekday'] = self.df['InvoiceDate'].dt.weekday  # 0=Monday

                self.transformation_rules.append({
                    'rule': 'Standardize dates and extract features',
                    'description': 'Added Year, Month, Day, Hour, DayOfWeek columns'
                })

                print(f"   - Column InvoiceDate transformed to datetime and extracted time features")

            except Exception as e:
                print(f"   Error to transform date: {e}")

    def calculate_total_price(self):
        """Calculate TotalPrice = Quantity × UnitPrice"""
        if 'Quantity' in self.df.columns and 'UnitPrice' in self.df.columns:
            self.df['TotalPrice'] = self.df['Quantity'] * self.df['UnitPrice']

            self.transformation_rules.append({
                'rule': 'Calculate TotalPrice',
                'formula': 'Quantity × UnitPrice'
            })

            # Sales statistics
            total_sales = self.df['TotalPrice'].sum()
            avg_sale = self.df['TotalPrice'].mean()

            print(f"   - Add column TotalPrice")
            print(f"   - Total Sale: £{total_sales:,.2f}")
            print(f"   - Mean each transaction: £{avg_sale:,.2f}")

    def get_cleaning_summary(self):
        """Final cleaning summary"""
        return {
            'initial_rows': self.stats_before['rows'],
            'final_rows': len(self.df),
            'rows_removed': self.stats_before['rows'] - len(self.df),
            'transformations': len(self.transformation_rules),
            'transformation_rules': self.transformation_rules,
            'cleaning_log': self.cleaning_log,
            'columns_added': list(set(self.df.columns) - set(['InvoiceNo', 'StockCode', 'Description',
                                                              'Quantity', 'InvoiceDate', 'UnitPrice',
                                                              'CustomerID', 'Country']))
        }