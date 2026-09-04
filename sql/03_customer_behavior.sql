-- ============================================================
-- CREDIT CARD CUSTOMER ANALYTICS
-- SQL CUSTOMER BEHAVIOR ANALYSIS
-- ============================================================


-- 1. Transaction activity and attrition

SELECT
    Attrition_Flag,

    COUNT(*) AS customer_count,

    ROUND(AVG(Total_Trans_Ct), 2) AS avg_transaction_count,

    ROUND(AVG(Total_Trans_Amt), 2) AS avg_transaction_amount,

    ROUND(AVG(Total_Ct_Chng_Q4_Q1), 3) AS avg_transaction_count_change,

    ROUND(AVG(Total_Amt_Chng_Q4_Q1), 3) AS avg_transaction_amount_change

FROM customers

GROUP BY Attrition_Flag;


-- 2. Customer engagement segments

SELECT
    CASE
        WHEN Total_Trans_Ct < 40 THEN 'Low Engagement'
        WHEN Total_Trans_Ct < 80 THEN 'Medium Engagement'
        ELSE 'High Engagement'
    END AS engagement_segment,

    COUNT(*) AS customer_count,

    SUM(
        CASE
            WHEN Attrition_Flag = 'Attrited Customer'
            THEN 1
            ELSE 0
        END
    ) AS attrited_customers,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN Attrition_Flag = 'Attrited Customer'
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS attrition_rate

FROM customers

GROUP BY engagement_segment

ORDER BY attrition_rate DESC;


-- 3. Inactivity and attrition

SELECT
    Months_Inactive_12_mon AS months_inactive,

    COUNT(*) AS customer_count,

    SUM(
        CASE
            WHEN Attrition_Flag = 'Attrited Customer'
            THEN 1
            ELSE 0
        END
    ) AS attrited_customers,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN Attrition_Flag = 'Attrited Customer'
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS attrition_rate

FROM customers

GROUP BY Months_Inactive_12_mon

ORDER BY months_inactive;


-- 4. Customer contacts and attrition

SELECT
    Contacts_Count_12_mon AS customer_contacts,

    COUNT(*) AS customer_count,

    ROUND(AVG(Months_Inactive_12_mon), 2)
        AS avg_months_inactive,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN Attrition_Flag = 'Attrited Customer'
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS attrition_rate

FROM customers

GROUP BY Contacts_Count_12_mon

ORDER BY customer_contacts;


-- 5. Utilization and attrition

SELECT
    CASE
        WHEN Avg_Utilization_Ratio < 0.10 THEN 'Very Low Utilization'
        WHEN Avg_Utilization_Ratio < 0.30 THEN 'Low Utilization'
        WHEN Avg_Utilization_Ratio < 0.60 THEN 'Moderate Utilization'
        ELSE 'High Utilization'
    END AS utilization_segment,

    COUNT(*) AS customer_count,

    ROUND(AVG(Credit_Limit), 2) AS avg_credit_limit,

    ROUND(AVG(Total_Revolving_Bal), 2)
        AS avg_revolving_balance,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN Attrition_Flag = 'Attrited Customer'
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS attrition_rate

FROM customers

GROUP BY utilization_segment

ORDER BY attrition_rate DESC;