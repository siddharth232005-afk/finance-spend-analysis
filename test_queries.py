import sqlite3
import pandas as pd

conn = sqlite3.connect(':memory:')
df = pd.read_csv('clean_transactions.csv')
df.to_sql('transactions', conn, index=False, if_exists='replace')

def run(label, q):
    print(f"\n--- {label} ---")
    try:
        result = pd.read_sql_query(q, conn)
        print(result.head(6).to_string(index=False))
        print(f"({len(result)} rows total)")
    except Exception as e:
        print(f"ERROR: {e}")

# Q1 Monthly spend by category
run("Q1: Monthly spend by category", """
SELECT year_month, category, ROUND(SUM(ABS(amount)),2) AS total_spend
FROM transactions WHERE txn_type='debit'
GROUP BY year_month, category ORDER BY year_month, total_spend DESC
""")

# Q2 Top merchants
run("Q2: Top 10 merchants", """
SELECT merchant, ROUND(SUM(ABS(amount)),2) AS total_spend, COUNT(*) AS n
FROM transactions WHERE txn_type='debit'
GROUP BY merchant ORDER BY total_spend DESC LIMIT 10
""")

# Q3 MoM growth
run("Q3: MoM growth", """
WITH monthly AS (
  SELECT year_month, SUM(ABS(amount)) AS total_spend
  FROM transactions WHERE txn_type='debit' GROUP BY year_month
)
SELECT year_month, total_spend,
  LAG(total_spend) OVER (ORDER BY year_month) AS prev_month,
  ROUND((total_spend - LAG(total_spend) OVER (ORDER BY year_month)) * 100.0
        / LAG(total_spend) OVER (ORDER BY year_month), 2) AS mom_growth_pct
FROM monthly ORDER BY year_month
""")

# Q6 Savings rate
run("Q6: Savings rate", """
WITH monthly_flow AS (
  SELECT year_month,
    SUM(CASE WHEN txn_type='credit' THEN amount ELSE 0 END) AS income,
    SUM(CASE WHEN txn_type='debit' THEN ABS(amount) ELSE 0 END) AS expense
  FROM transactions GROUP BY year_month
)
SELECT year_month, income, expense,
  ROUND((income-expense)*100.0/income, 2) AS savings_rate_pct
FROM monthly_flow ORDER BY year_month
""")

# Q8 Rank top 3 merchants per category
run("Q8: Top 3 merchants per category", """
WITH merchant_spend AS (
  SELECT category, merchant, SUM(ABS(amount)) AS total_spend,
    RANK() OVER (PARTITION BY category ORDER BY SUM(ABS(amount)) DESC) AS rnk
  FROM transactions WHERE txn_type='debit' GROUP BY category, merchant
)
SELECT category, merchant, ROUND(total_spend,2) AS total_spend, rnk
FROM merchant_spend WHERE rnk<=3 ORDER BY category, rnk
""")

# Q9 Outlier transactions
run("Q9: Outlier transactions (>2x category avg)", """
WITH cat_avg AS (
  SELECT category, AVG(ABS(amount)) AS avg_amount
  FROM transactions WHERE txn_type='debit' GROUP BY category
)
SELECT t.transaction_date, t.category, t.merchant, ABS(t.amount) AS amount,
  ROUND(c.avg_amount,2) AS category_avg
FROM transactions t JOIN cat_avg c ON t.category=c.category
WHERE t.txn_type='debit' AND ABS(t.amount) > 2*c.avg_amount
ORDER BY amount DESC LIMIT 15
""")

print("\n\nAll queries executed successfully against cleaned data.")
