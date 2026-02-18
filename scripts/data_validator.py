# scripts/data_validator.py

import pandas as pd
from datetime import datetime


class DataValidator:
    """Check data validator Online Retail"""

    def __init__(self, df):
        self.df = df.copy()
        self.issues = []
        self.validation_report = {}

    def run_all_checks(self):
        """Run all validity checks"""
        print("\n" + "=" * 50)
        print("Step2: check data validator")
        print("=" * 50)

        self.check_completeness()
        self.check_consistency()
        self.check_accuracy()
        self.check_business_rules()

        print(f"\nsummary of detected issues: {len(self.issues)}")
        for i, issue in enumerate(self.issues[:5], 1):  # Display the first 5 issues
            print(f"   {i}. {issue['type']}: {issue['message']}")

        if len(self.issues) > 5:
            print(f"   ... and {len(self.issues) - 5} other issues")

        return self.issues

    def check_completeness(self):
        """check null values (Completeness)"""
        missing = self.df.isnull().sum()
        missing_percent = (missing / len(self.df)) * 100

        result = {}
        for col in self.df.columns:
            if missing[col] > 0:
                result[col] = {
                    'count': int(missing[col]),
                    'percent': round(missing_percent[col], 2)
                }

                #If it has more than %5 missing value, record it as an issue
                if missing_percent[col] > 5:
                    self.issues.append({
                        'type': 'high_missing',
                        'severity': 'high' if missing_percent[col] > 20 else 'medium',
                        'column': col,
                        'message': f"{col}: {missing[col]:,} missing values ({missing_percent[col]:.1f}%)"
                    })

        self.validation_report['completeness'] = result

    def check_consistency(self):
        """Check Consistency (duplicated and uniformity)"""
        result = {}

        # Check duplicated
        duplicate_rows = self.df.duplicated().sum()
        duplicate_percent = (duplicate_rows / len(self.df)) * 100

        result['duplicate_rows'] = int(duplicate_rows)
        result['duplicate_percent'] = round(duplicate_percent, 2)

        if duplicate_rows > 0:
            self.issues.append({
                'type': 'duplicates',
                'severity': 'high' if duplicate_percent > 5 else 'low',
                'message': f"{duplicate_rows:,} duplicate rows ({duplicate_percent:.1f}%)"
            })

        #Check column Description for odd value
        if 'Description' in self.df.columns:
            # samples that start with numbers (repeated rows)
            odd_desc = self.df[~self.df['Description'].astype(str).str[0].str.isalpha()].shape[0]
            if odd_desc > 100:
                self.issues.append({
                    'type': 'inconsistent_format',
                    'severity': 'low',
                    'column': 'Description',
                    'message': f"{odd_desc} record with odd description (starts with number or special character)"
                })

        self.validation_report['consistency'] = result

    def check_accuracy(self):
        """Check Accuracy (logical value)"""
        result = {}

        # Check Quantity negative (return product)
        if 'Quantity' in self.df.columns:
            negative_qty = (self.df['Quantity'] < 0).sum()
            negative_percent = (negative_qty / len(self.df)) * 100

            result['negative_quantity'] = int(negative_qty)
            result['negative_percent'] = round(negative_percent, 2)

            if negative_qty > 0:
                self.issues.append({
                    'type': 'returns',
                    'severity': 'info',
                    'message': f"{negative_qty:,} record with Quantity negative (return product) - {negative_percent:.1f}%"
                })

        # Check UnitPrice zero or negative
        if 'UnitPrice' in self.df.columns:
            zero_price = (self.df['UnitPrice'] <= 0).sum()

            result['invalid_price'] = int(zero_price)

            if zero_price > 0:
                self.issues.append({
                    'type': 'invalid_price',
                    'severity': 'high',
                    'message': f"{zero_price} record with zero or negative price"
                })

        # Check CustomerID null (important for analysing customers)
        if 'CustomerID' in self.df.columns:
            missing_customer = self.df['CustomerID'].isnull().sum()
            missing_percent = (missing_customer / len(self.df)) * 100

            result['missing_customer'] = int(missing_customer)
            result['missing_customer_percent'] = round(missing_percent, 2)

            if missing_customer > 0:
                self.issues.append({
                    'type': 'missing_customer',
                    'severity': 'high' if missing_percent > 30 else 'medium',
                    'message': f"{missing_customer:,} without record CustomerID ({missing_percent:.1f}%)"
                })

        self.validation_report['accuracy'] = result

    def check_business_rules(self):
        """Check business rules for dataset Online Retail"""
        result = {}

        # Cancel invoices (starts with C)
        if 'InvoiceNo' in self.df.columns:
            cancelled = self.df['InvoiceNo'].astype(str).str.startswith('C').sum()
            result['cancelled_invoices'] = int(cancelled)

            if cancelled > 0:
                self.issues.append({
                    'type': 'cancelled_transactions',
                    'severity': 'info',
                    'message': f"{cancelled} canceled invoices (starts with C)"
                })

        # special StockCodes (M manual، S and samples...)
        if 'StockCode' in self.df.columns:
            special_codes = self.df[self.df['StockCode'].astype(str).str.match(r'^[A-Z]')].shape[0]
            result['special_stockcodes'] = int(special_codes)

        self.validation_report['business_rules'] = result

    def get_summary(self):
        """Final result validation"""
        return {
            'total_issues': len(self.issues),
            'issues': self.issues,
            'validation_report': self.validation_report
        }