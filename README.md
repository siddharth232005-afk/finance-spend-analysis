# Personal Finance Spend Analysis (End-to-End DA Project)

## Overview
An end-to-end data analysis project on a year of personal financial transactions
(July 2024 – June 2025). Covers data generation/cleaning in Python, storage and
querying in PostgreSQL, and visualization with matplotlib.

**Note on data:** Since real bank transaction exports are hard to source publicly
with clean labels, this dataset was synthetically generated in Python to mirror
the structure and messiness (duplicates, missing values, inconsistent casing) of
real transaction data. All analysis and cleaning logic is applied exactly as it
would be on a real export.

## Tech Stack
- **Python** (pandas) — data generation & cleaning
- **PostgreSQL** — storage and analytical SQL queries
- **matplotlib** — visualization

## Project Structure
```
finance_project/
├── generate_data.py           # synthetic data generator
├── raw_transactions.csv       # raw (messy) data
├── clean_data.py              # cleaning script
├── clean_transactions.csv     # cleaned data
├── schema.sql                 # Postgres table schema
├── queries.sql                # 10 analytical SQL queries
├── make_charts.py             # chart generation
├── chart1_monthly_category_spend.png
├── chart2_category_totals.png
├── chart3_income_vs_expense.png
└── README.md
```

## Data Cleaning Steps
1. Removed duplicate transactions (matched on date + category + merchant + amount)
2. Standardized inconsistent category casing (e.g. `GROCERIES` → `Groceries`)
3. Filled missing merchant values with `'Unknown'` instead of dropping rows,
   to avoid losing real transaction amounts from the analysis
4. Converted transaction date to proper `date` type
5. Added derived columns: `year_month`, `day_of_week`, `month_name` for
   easier grouping in SQL

## SQL Analysis (queries.sql)
10 queries covering core DA skills:
1. Monthly spend by category
2. Top 10 merchants by total spend
3. Month-over-month spend growth (window function: `LAG`)
4. Recurring vs one-time transaction split
5. Average spend by day of week
6. Monthly savings rate (income vs expense)
7. Category share of total spend (window function: `SUM() OVER()`)
8. Top 3 merchants per category (window function: `RANK()`)
9. Outlier transactions (>2x category average)
10. Running cumulative spend over time (window function: `SUM() OVER (ORDER BY ...)`)

## Key Findings
- Groceries and Dining together account for the largest share of monthly spend.
- Savings rate varied month to month (roughly 4%–31%), with the lowest savings
  months coinciding with higher one-time Shopping/Education spend.
- A small number of merchants (Amazon, Flipkart, Myntra, BigBasket, DMart)
  drive a disproportionate share of total spend — the classic 80/20 pattern.
- Spend is fairly stable month-to-month (±15%) apart from occasional spikes
  tied to one-time education/shopping expenses.

## How to Run
```bash
# 1. Generate & clean data
python3 generate_data.py
python3 clean_data.py

# 2. Load into Postgres
psql -U <user> -d <dbname> -f schema.sql
psql -U <user> -d <dbname> -c "\copy transactions FROM 'clean_transactions.csv' WITH CSV HEADER"

# 3. Run analysis
psql -U <user> -d <dbname> -f queries.sql

# 4. Generate charts
python3 make_charts.py
```

