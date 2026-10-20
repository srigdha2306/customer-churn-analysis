
SELECT
    COUNT(*) AS total_customers
FROM customers;

SELECT
    COUNT(*) AS churned_customers
FROM customers
WHERE Churn = 'Yes';

SELECT
    COUNT(*) AS retained_customers
FROM customers
WHERE Churn = 'No';

SELECT
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS churn_percentage
FROM customers;

SELECT
    Contract,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS churn_percentage
FROM customers
GROUP BY Contract
ORDER BY churn_percentage DESC;

SELECT
    PaymentMethod,
    COUNT(*) AS total_customers,
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS churn_percentage
FROM customers
GROUP BY PaymentMethod
ORDER BY churn_percentage DESC;


SELECT
    SeniorCitizen,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS churn_percentage
FROM customers
GROUP BY SeniorCitizen
ORDER BY churn_percentage DESC;


SELECT
    Partner,
    Dependents,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS churn_percentage
FROM customers
GROUP BY Partner, Dependents
ORDER BY churn_percentage DESC;


SELECT
    CASE
        WHEN tenure <= 12 THEN '0-12 months'
        WHEN tenure <= 24 THEN '13-24 months'
        WHEN tenure <= 48 THEN '25-48 months'
        ELSE '49-72 months'
    END AS tenure_group,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS churn_percentage
FROM customers
GROUP BY
    CASE
        WHEN tenure <= 12 THEN '0-12 months'
        WHEN tenure <= 24 THEN '13-24 months'
        WHEN tenure <= 48 THEN '25-48 months'
        ELSE '49-72 months'
    END
ORDER BY MIN(tenure);


SELECT
    CASE
        WHEN MonthlyCharges > (
            SELECT AVG(MonthlyCharges)
            FROM customers
        ) THEN 'Above average'
        ELSE 'At or below average'
    END AS charge_group,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS churn_percentage
FROM customers
GROUP BY charge_group
ORDER BY churn_percentage DESC;


WITH customer_charge_groups AS (
    SELECT
        CASE
            WHEN MonthlyCharges > (
                SELECT AVG(MonthlyCharges)
                FROM customers
            ) THEN 'Above average'
            ELSE 'At or below average'
        END AS charge_group,
        Churn
    FROM customers
)
SELECT
    charge_group,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS churn_percentage
FROM customer_charge_groups
GROUP BY charge_group
ORDER BY churn_percentage DESC;


SELECT
    customerID,
    MonthlyCharges,
    ROUND(
        AVG(MonthlyCharges) OVER (),
        2
    ) AS overall_avg_charge,
    ROUND(
        MonthlyCharges - AVG(MonthlyCharges) OVER (),
        2
    ) AS difference_from_average
FROM customers
LIMIT 10;


SELECT
    customerID,
    Contract,
    MonthlyCharges,
    ROUND(
        AVG(MonthlyCharges) OVER (
            PARTITION BY Contract
        ),
        2
    ) AS contract_avg_charge,
    ROUND(
        MonthlyCharges - AVG(MonthlyCharges) OVER (
            PARTITION BY Contract
        ),
        2
    ) AS difference_from_contract_avg
FROM customers
LIMIT 15;


WITH contract_churn AS (
    SELECT
        Contract,
        COUNT(*) AS total_customers,
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
            AS churned_customers,
        ROUND(
            100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
            / COUNT(*),
            2
        ) AS churn_percentage
    FROM customers
    GROUP BY Contract
)
SELECT
    Contract,
    total_customers,
    churned_customers,
    churn_percentage,
    RANK() OVER (
        ORDER BY churn_percentage DESC
    ) AS churn_rank
FROM contract_churn
ORDER BY churn_rank;


WITH customer_segments AS (
    SELECT
        Contract,
        CASE
            WHEN tenure <= 12 THEN '0-12 months'
            WHEN tenure <= 24 THEN '13-24 months'
            WHEN tenure <= 48 THEN '25-48 months'
            ELSE '49-72 months'
        END AS tenure_group,
        Churn
    FROM customers
)
SELECT
    Contract,
    tenure_group,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        AS churned_customers,
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS churn_percentage
FROM customer_segments
GROUP BY Contract, tenure_group
ORDER BY churn_percentage DESC;


WITH overall AS (
    SELECT
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
        / COUNT(*) AS overall_churn_percentage
    FROM customers
),
segments AS (
    SELECT
        Contract,
        CASE
            WHEN tenure <= 12 THEN '0-12 months'
            WHEN tenure <= 24 THEN '13-24 months'
            WHEN tenure <= 48 THEN '25-48 months'
            ELSE '49-72 months'
        END AS tenure_group,
        COUNT(*) AS total_customers,
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)
            AS churned_customers
    FROM customers
    GROUP BY Contract, tenure_group
)
SELECT
    Contract,
    tenure_group,
    total_customers,
    churned_customers,
    ROUND(
        100.0 * churned_customers / total_customers,
        2
    ) AS segment_churn_percentage,
    ROUND(overall_churn_percentage, 2) AS overall_churn_percentage,
    ROUND(
        100.0 * churned_customers / total_customers
        - overall_churn_percentage,
        2
    ) AS percentage_point_difference
FROM segments
CROSS JOIN overall
ORDER BY percentage_point_difference DESC;

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT customerID) AS unique_customers,
    SUM(CASE WHEN customerID IS NULL THEN 1 ELSE 0 END)
        AS missing_customer_ids,
    SUM(CASE WHEN Churn IS NULL THEN 1 ELSE 0 END)
        AS missing_churn_values
FROM customers;


SELECT
    SUM(CASE WHEN tenure < 0 THEN 1 ELSE 0 END)
        AS negative_tenure,
    SUM(CASE WHEN MonthlyCharges < 0 THEN 1 ELSE 0 END)
        AS negative_monthly_charges,
    SUM(CASE WHEN TotalCharges < 0 THEN 1 ELSE 0 END)
        AS negative_total_charges,
    SUM(CASE WHEN tenure > 72 THEN 1 ELSE 0 END)
        AS tenure_over_72_months,
    SUM(CASE WHEN Churn NOT IN ('Yes', 'No') THEN 1 ELSE 0 END)
        AS invalid_churn_values
FROM customers;


SELECT
    COUNT(*) AS missing_total_charges,
    SUM(
        CASE WHEN tenure = 0 THEN 1 ELSE 0 END
    ) AS missing_with_zero_tenure,
    SUM(
        CASE WHEN tenure > 0 THEN 1 ELSE 0 END
    ) AS missing_with_positive_tenure
FROM customers
WHERE TotalCharges IS NULL;
