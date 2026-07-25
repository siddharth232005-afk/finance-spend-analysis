import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# Categories with realistic merchant lists and typical amount ranges
categories = {
    'Groceries':    {'merchants': ['BigBasket', 'DMart', 'Reliance Fresh', 'Local Kirana'], 'range': (150, 700)},
    'Rent':         {'merchants': ['Landlord Transfer'], 'range': (8000, 10000)},
    'Dining':       {'merchants': ['Zomato', 'Swiggy', 'Domino\'s', 'Cafe Coffee Day', 'McDonalds'], 'range': (100, 400)},
    'Utilities':    {'merchants': ['Electricity Board', 'Airtel Broadband', 'Jio Recharge', 'Water Dept'], 'range': (200, 1000)},
    'Entertainment':{'merchants': ['Netflix', 'Spotify', 'BookMyShow', 'PVR Cinemas'], 'range': (150, 500)},
    'Transport':    {'merchants': ['Uber', 'Ola', 'Metro Card', 'Petrol Pump'], 'range': (50, 400)},
    'Shopping':     {'merchants': ['Amazon', 'Flipkart', 'Myntra', 'Local Store'], 'range': (200, 1500)},
    'Healthcare':   {'merchants': ['Apollo Pharmacy', 'Local Clinic', 'Health Insurance'], 'range': (100, 1200)},
    'Education':    {'merchants': ['Udemy', 'Coursera', 'College Fee'], 'range': (300, 2000)},
    'Salary':       {'merchants': ['Employer Inc'], 'range': (50000, 65000)},
}

start_date = datetime(2024, 7, 1)
end_date = datetime(2025, 6, 30)
date_range = (end_date - start_date).days

rows = []
txn_id = 1

# Generate salary as recurring monthly income (1st of every month)
current = start_date
while current <= end_date:
    salary_amt = round(np.random.uniform(*categories['Salary']['range']), 2)
    rows.append([txn_id, current.strftime('%Y-%m-%d'), 'Salary', 'Employer Inc', salary_amt, 'credit'])
    txn_id += 1
    # move to 1st of next month
    if current.month == 12:
        current = current.replace(year=current.year+1, month=1)
    else:
        current = current.replace(month=current.month+1)

# Generate rent as recurring monthly expense (5th of every month)
current = start_date
while current <= end_date:
    rent_date = current.replace(day=5)
    if rent_date <= end_date:
        rent_amt = round(np.random.uniform(*categories['Rent']['range']), 2)
        rows.append([txn_id, rent_date.strftime('%Y-%m-%d'), 'Rent', 'Landlord Transfer', -rent_amt, 'debit'])
        txn_id += 1
    if current.month == 12:
        current = current.replace(year=current.year+1, month=1)
    else:
        current = current.replace(month=current.month+1)

# Generate random day-to-day transactions across other categories
spend_categories = [c for c in categories if c not in ('Salary', 'Rent')]
n_random_txns = 1000

for _ in range(n_random_txns):
    day_offset = np.random.randint(0, date_range)
    txn_date = start_date + timedelta(days=int(day_offset))
    cat = np.random.choice(spend_categories, p=[0.28, 0.20, 0.10, 0.14, 0.08, 0.12, 0.05, 0.03])
    merchant = np.random.choice(categories[cat]['merchants'])
    amt = round(np.random.uniform(*categories[cat]['range']), 2)
    rows.append([txn_id, txn_date.strftime('%Y-%m-%d'), cat, merchant, -amt, 'debit'])
    txn_id += 1

df = pd.DataFrame(rows, columns=['transaction_id', 'transaction_date', 'category', 'merchant', 'amount', 'txn_type'])
df = df.sort_values('transaction_date').reset_index(drop=True)
df['transaction_id'] = range(1, len(df) + 1)

# Introduce some realistic messiness for the cleaning step (nulls, dupes, inconsistent casing)
dupe_rows = df.sample(15, random_state=1)
df = pd.concat([df, dupe_rows], ignore_index=True)

null_idx = df.sample(30, random_state=2).index
df.loc[null_idx, 'merchant'] = None

case_idx = df.sample(200, random_state=3).index
df.loc[case_idx, 'category'] = df.loc[case_idx, 'category'].str.upper()

df.to_csv('raw_transactions.csv', index=False)
print(f"Generated {len(df)} rows -> raw_transactions.csv")
print(df.head())
print(df['category'].value_counts())
