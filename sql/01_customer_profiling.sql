-- ============================================================
-- CREDIT CARD CUSTOMER ANALYTICS
-- SQL CUSTOMER PROFILING
-- ============================================================

-- 1. Overall portfolio profile
SELECT
    COUNT(*) AS total_customers,
    ROUND(AVG(Customer_Age), 2) AS avg_customer_age,
    ROUND(AVG(Credit_Limit), 2) AS avg_credit_limit,
    ROUND(AVG(Total_Trans_Amt), 2) AS avg_transaction_amount,
    ROUND(AVG(Total_Trans_Ct), 2) AS avg_transaction_count,
    ROUND(AVG(Avg_Utilization_Ratio), 2) AS avg_utilization
FROM customers;


-- 2. Customer distribution by gender
SELECT
    Gender,
    COUNT(*) AS customer_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM customers), 2)
        AS percentage_of_customers
FROM customers
GROUP BY Gender
ORDER BY customer_count DESC;


-- 3. Customer distribution by card category
SELECT
    Card_Category,
    COUNT(*) AS customer_count,
    ROUND(AVG(Credit_Limit), 2) AS avg_credit_limit,
    ROUND(AVG(Total_Trans_Amt), 2) AS avg_transaction_amount
FROM customers
GROUP BY Card_Category
ORDER BY customer_count DESC;


-- 4. Customer distribution by income category
SELECT
    Income_Category,
    COUNT(*) AS customer_count,
    ROUND(AVG(Credit_Limit), 2) AS avg_credit_limit
FROM customers
GROUP BY Income_Category
ORDER BY customer_count DESC;