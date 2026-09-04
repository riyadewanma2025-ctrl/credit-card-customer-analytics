-- ============================================================
-- CREDIT CARD CUSTOMER ANALYTICS
-- SQL RISK ANALYSIS
-- ============================================================


-- 1. Risk category profile

SELECT
    Risk_Category,
    COUNT(*) AS customer_count,

    ROUND(AVG(Churn_Probability) * 100, 2)
        AS avg_predicted_churn_probability,

    ROUND(AVG(Credit_Limit), 2)
        AS avg_credit_limit,

    ROUND(AVG(Total_Trans_Amt), 2)
        AS avg_transaction_amount,

    ROUND(AVG(Total_Trans_Ct), 2)
        AS avg_transaction_count

FROM dashboard

GROUP BY Risk_Category

ORDER BY avg_predicted_churn_probability DESC;


-- 2. Customer segment and risk

SELECT
    Customer_Segment,
    Risk_Category,

    COUNT(*) AS customer_count,

    ROUND(AVG(Churn_Probability) * 100, 2)
        AS avg_predicted_churn_probability,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN Attrition = 1
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS actual_attrition_rate

FROM dashboard

GROUP BY
    Customer_Segment,
    Risk_Category

ORDER BY
    Customer_Segment,
    avg_predicted_churn_probability DESC;


-- 3. High-risk customers by customer segment

SELECT
    Customer_Segment,

    COUNT(*) AS high_risk_customers,

    ROUND(AVG(Credit_Limit), 2)
        AS avg_credit_limit,

    ROUND(AVG(Total_Trans_Amt), 2)
        AS avg_transaction_amount,

    ROUND(AVG(Total_Trans_Ct), 2)
        AS avg_transaction_count,

    ROUND(AVG(Avg_Utilization_Ratio), 3)
        AS avg_utilization

FROM dashboard

WHERE Risk_Category = 'High Risk'

GROUP BY Customer_Segment

ORDER BY high_risk_customers DESC;


-- 4. High-risk customer prioritization

SELECT
    CLIENTNUM,
    Customer_Segment,
    Risk_Category,
    Churn_Probability,
    Credit_Limit,
    Total_Trans_Amt,
    Total_Trans_Ct,
    Months_Inactive_12_mon,
    Contacts_Count_12_mon,
    Avg_Utilization_Ratio,
    Attrition

FROM dashboard

WHERE Risk_Category = 'High Risk'

ORDER BY
    Churn_Probability DESC

LIMIT 20;