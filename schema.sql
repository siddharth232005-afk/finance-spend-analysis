-- Run this in your Postgres (psql or pgAdmin)
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id   INTEGER PRIMARY KEY,
    transaction_date DATE NOT NULL,
    category         VARCHAR(50) NOT NULL,
    merchant         VARCHAR(100),
    amount           NUMERIC(10,2) NOT NULL,
    txn_type         VARCHAR(10) NOT NULL,
    year_month       VARCHAR(7),
    day_of_week      VARCHAR(15),
    month_name       VARCHAR(15)
);
