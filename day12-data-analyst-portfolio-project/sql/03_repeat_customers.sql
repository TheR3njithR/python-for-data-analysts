-- Q3: how much revenue comes from repeat customers (2+ orders)?
WITH c AS (
    SELECT customer_id, COUNT(DISTINCT order_id) AS n, SUM(revenue) AS rev
    FROM orders GROUP BY customer_id
)
SELECT ROUND(100.0 * AVG(n >= 2), 1) AS repeat_pct_of_customers,
       ROUND(100.0 * SUM(CASE WHEN n >= 2 THEN rev END) / SUM(rev), 1) AS repeat_pct_of_revenue
FROM c;
