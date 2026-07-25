-- =====================================================
-- Q1: Monthly spend by category (excluding income)
-- =====================================================
SELECT year_month, category, ROUND(SUM(ABS(amount))::numeric, 2) AS total_spend
FROM transactions
WHERE txn_type = 'debit'
GROUP BY year_month, category
ORDER BY year_month, total_spend DESC;

-- =====================================================
-- Q2: Top 10 merchants by total spend
-- =====================================================
SELECT merchant, ROUND(SUM(ABS(amount))::numeric, 2) AS total_spend, COUNT(*) AS num_transactions
FROM transactions
WHERE txn_type = 'debit'
GROUP BY merchant
ORDER BY total_spend DESC
LIMIT 10;

-- =====================================================
-- Q3: Month-over-month total spend growth %
-- =====================================================
WITH monthly AS (
    SELECT year_month, SUM(ABS(amount)) AS total_spend
    FROM transactions
    WHERE txn_type = 'debit'
    GROUP BY year_month
)
SELECT year_month,
       total_spend,
       LAG(total_spend) OVER (ORDER BY year_month) AS prev_month_spend,
       ROUND(
           ((total_spend - LAG(total_spend) OVER (ORDER BY year_month))
           / LAG(total_spend) OVER (ORDER BY year_month) * 100)::numeric, 2
       ) AS mom_growth_pct
FROM monthly
ORDER BY year_month;

-- =====================================================
-- Q4: Recurring (Rent, Salary) vs one-time spend split
-- =====================================================
SELECT
    CASE WHEN category IN ('Rent','Salary') THEN 'Recurring' ELSE 'One-time' END AS txn_group,
    ROUND(SUM(ABS(amount))::numeric, 2) AS total_amount,
    COUNT(*) AS num_transactions
FROM transactions
GROUP BY txn_group;

-- =====================================================
-- Q5: Highest average spend by day of week
-- =====================================================
SELECT day_of_week, ROUND(AVG(ABS(amount))::numeric, 2) AS avg_spend, COUNT(*) AS num_transactions
FROM transactions
WHERE txn_type = 'debit'
GROUP BY day_of_week
ORDER BY avg_spend DESC;

-- =====================================================
-- Q6: Savings rate per month (income - expense) / income
-- =====================================================
WITH monthly_flow AS (
    SELECT year_month,
           SUM(CASE WHEN txn_type = 'credit' THEN amount ELSE 0 END) AS income,
           SUM(CASE WHEN txn_type = 'debit' THEN ABS(amount) ELSE 0 END) AS expense
    FROM transactions
    GROUP BY year_month
)
SELECT year_month, income, expense,
       ROUND(((income - expense) / income * 100)::numeric, 2) AS savings_rate_pct
FROM monthly_flow
ORDER BY year_month;

-- =====================================================
-- Q7: Category share of total spend (%)
-- =====================================================
SELECT category,
       ROUND(SUM(ABS(amount))::numeric, 2) AS total_spend,
       ROUND((SUM(ABS(amount)) * 100.0 / SUM(SUM(ABS(amount))) OVER())::numeric, 2) AS pct_of_total
FROM transactions
WHERE txn_type = 'debit'
GROUP BY category
ORDER BY total_spend DESC;

-- =====================================================
-- Q8: Rank top 3 merchants within each category (window function)
-- =====================================================
WITH merchant_spend AS (
    SELECT category, merchant, SUM(ABS(amount)) AS total_spend,
           RANK() OVER (PARTITION BY category ORDER BY SUM(ABS(amount)) DESC) AS rnk
    FROM transactions
    WHERE txn_type = 'debit'
    GROUP BY category, merchant
)
SELECT category, merchant, ROUND(total_spend::numeric, 2) AS total_spend, rnk
FROM merchant_spend
WHERE rnk <= 3
ORDER BY category, rnk;

-- =====================================================
-- Q9: Transactions above 2x their category's average (outlier spend)
-- =====================================================
WITH cat_avg AS (
    SELECT category, AVG(ABS(amount)) AS avg_amount
    FROM transactions
    WHERE txn_type = 'debit'
    GROUP BY category
)
SELECT t.transaction_date, t.category, t.merchant, ABS(t.amount) AS amount, ROUND(c.avg_amount::numeric,2) AS category_avg
FROM transactions t
JOIN cat_avg c ON t.category = c.category
WHERE t.txn_type = 'debit' AND ABS(t.amount) > 2 * c.avg_amount
ORDER BY amount DESC
LIMIT 15;

-- =====================================================
-- Q10: Running total of expenses over time (cumulative spend)
-- =====================================================
SELECT transaction_date, category, ABS(amount) AS amount,
       SUM(ABS(amount)) OVER (ORDER BY transaction_date) AS cumulative_spend
FROM transactions
WHERE txn_type = 'debit'
ORDER BY transaction_date
LIMIT 20;
