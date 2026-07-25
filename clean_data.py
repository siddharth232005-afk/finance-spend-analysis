import pandas as pd

df = pd.read_csv('raw_transactions.csv')
print("BEFORE CLEANING")
print(f"Rows: {len(df)}")
print(f"Duplicates: {df.duplicated(subset=['transaction_date','category','merchant','amount']).sum()}")
print(f"Nulls in merchant: {df['merchant'].isna().sum()}")
print(f"Unique category values (messy): {df['category'].nunique()}")
print()

# 1. Remove duplicate transactions (same date+category+merchant+amount = same txn logged twice)
df = df.drop_duplicates(subset=['transaction_date','category','merchant','amount'])

# 2. Standardize category casing (GROCERIES -> Groceries)
df['category'] = df['category'].str.strip().str.title()

# 3. Fill missing merchant with 'Unknown' rather than dropping the row (we don't want to lose real spend data)
df['merchant'] = df['merchant'].fillna('Unknown')

# 4. Convert date column to proper datetime type
df['transaction_date'] = pd.to_datetime(df['transaction_date'])

# 5. Add helper columns used later for analysis
df['year_month'] = df['transaction_date'].dt.to_period('M').astype(str)
df['day_of_week'] = df['transaction_date'].dt.day_name()
df['month_name'] = df['transaction_date'].dt.strftime('%b %Y')

df = df.sort_values('transaction_date').reset_index(drop=True)
df['transaction_id'] = range(1, len(df) + 1)

print("AFTER CLEANING")
print(f"Rows: {len(df)}")
print(f"Unique category values: {sorted(df['category'].unique())}")
print(f"Nulls remaining: {df.isna().sum().sum()}")

df.to_csv('clean_transactions.csv', index=False)
print("\nSaved -> clean_transactions.csv")
