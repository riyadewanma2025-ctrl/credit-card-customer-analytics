-- ============================================================
-- CREDIT CARD CUSTOMER ANALYTICS
-- SQL ATTRITION ANALYSIS
-- ============================================================


-- 1. Overall attrition rate

SELECT
    Attrition_Flag,
    COUNT(*) AS customer_count,
    ROUND(
        100.0 * COUNT(*) / (SELECT COUNT(*) FROM customers),
        2
    ) AS percentage_of_customers
FROM customers
GROUP BY Attrition_Flag
ORDER BY customer_count DESC;


-- 2. Attrition by card category

SELECT
    Card_Category,
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

GROUP BY Card_Category

ORDER BY attrition_rate DESC;


-- 3. Attrition by income category

SELECT
    Income_Category,
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

GROUP BY Income_Category

ORDER BY attrition_rate DESC;


-- 4. Attrition by education level

SELECT
    Education_Level,
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

GROUP BY Education_Level

ORDER BY attrition_rate DESC;


-- 5. Attrition by marital status

SELECT
    Marital_Status,
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

GROUP BY Marital_Status

ORDER BY attrition_rate DESC;