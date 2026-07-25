import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('clean_transactions.csv')
df['transaction_date'] = pd.to_datetime(df['transaction_date'])

plt.style.use('seaborn-v0_8-whitegrid')

# Chart 1: Monthly spend by category (stacked bar)
spend = df[df['txn_type']=='debit']
monthly_cat = spend.groupby(['year_month','category'])['amount'].apply(lambda x: x.abs().sum()).unstack(fill_value=0)
fig, ax = plt.subplots(figsize=(11,6))
monthly_cat.plot(kind='bar', stacked=True, ax=ax, colormap='tab20')
ax.set_title('Monthly Spend by Category', fontsize=14, fontweight='bold')
ax.set_xlabel('Month'); ax.set_ylabel('Amount (INR)')
ax.legend(bbox_to_anchor=(1.02,1), loc='upper left', fontsize=8)
plt.tight_layout()
plt.savefig('chart1_monthly_category_spend.png', dpi=120)
plt.close()

# Chart 2: Category share pie/bar
cat_totals = spend.groupby('category')['amount'].apply(lambda x: x.abs().sum()).sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(9,6))
cat_totals.plot(kind='barh', ax=ax, color='#2b6cb0')
ax.set_title('Total Spend by Category (Full Year)', fontsize=14, fontweight='bold')
ax.set_xlabel('Amount (INR)')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('chart2_category_totals.png', dpi=120)
plt.close()

# Chart 3: Income vs Expense trend + savings rate
monthly_flow = df.groupby('year_month').apply(
    lambda g: pd.Series({
        'income': g.loc[g.txn_type=='credit','amount'].sum(),
        'expense': g.loc[g.txn_type=='debit','amount'].abs().sum()
    })
).reset_index()
fig, ax = plt.subplots(figsize=(11,6))
ax.plot(monthly_flow['year_month'], monthly_flow['income'], marker='o', label='Income', color='#2f855a', linewidth=2)
ax.plot(monthly_flow['year_month'], monthly_flow['expense'], marker='o', label='Expense', color='#c53030', linewidth=2)
ax.set_title('Monthly Income vs Expense', fontsize=14, fontweight='bold')
ax.set_xlabel('Month'); ax.set_ylabel('Amount (INR)')
plt.xticks(rotation=45)
ax.legend()
plt.tight_layout()
plt.savefig('chart3_income_vs_expense.png', dpi=120)
plt.close()

print("3 charts saved.")
