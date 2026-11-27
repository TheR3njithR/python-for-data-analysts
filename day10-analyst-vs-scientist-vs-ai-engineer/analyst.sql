-- Data analyst: what happened, and where?
SELECT plan, count(*) AS customers, round(100.0 * avg(churned), 1) AS churn_pct
FROM customers GROUP BY plan ORDER BY churn_pct DESC;

SELECT CASE WHEN support_calls >= 3 THEN '3+' ELSE CAST(support_calls AS TEXT) END AS calls,
       count(*) AS customers, round(100.0 * avg(churned), 1) AS churn_pct
FROM customers GROUP BY calls ORDER BY calls;
