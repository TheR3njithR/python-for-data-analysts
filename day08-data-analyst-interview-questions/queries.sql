-- name: q1_duplicates
-- Q1. Find duplicate customers (same email signed up more than once)
SELECT email, count(*) AS signups
FROM customers
GROUP BY email
HAVING count(*) > 1
ORDER BY email
LIMIT 5;

-- name: q1_duplicates_count
SELECT count(*) AS duplicate_emails FROM (
  SELECT email FROM customers GROUP BY email HAVING count(*) > 1
);

-- name: q2_second_highest
-- Q2. The second-highest order value (delivered orders)
SELECT max(o.qty * p.unit_price) AS second_highest
FROM orders o JOIN products p ON p.product_id = o.product_id
WHERE o.status = 'Delivered'
  AND o.qty * p.unit_price < (SELECT max(o2.qty * p2.unit_price)
                              FROM orders o2 JOIN products p2 ON p2.product_id = o2.product_id
                              WHERE o2.status = 'Delivered');

-- name: q2_top_values
SELECT DISTINCT o.qty * p.unit_price AS order_value
FROM orders o JOIN products p ON p.product_id = o.product_id
WHERE o.status = 'Delivered'
ORDER BY order_value DESC
LIMIT 3;

-- name: q3_top_per_city
-- Q3. The top customer in each city by delivered revenue (window function)
WITH rev AS (
  SELECT c.city, c.name, sum(o.qty * p.unit_price) AS revenue
  FROM orders o
  JOIN customers c ON c.customer_id = o.customer_id
  JOIN products p ON p.product_id = o.product_id
  WHERE o.status = 'Delivered'
  GROUP BY c.customer_id
)
SELECT city, name, revenue FROM (
  SELECT *, row_number() OVER (PARTITION BY city ORDER BY revenue DESC, name) AS rn FROM rev
) WHERE rn = 1
ORDER BY revenue DESC;

-- name: q4_mom_growth
-- Q4. Month-over-month revenue growth (LAG)
WITH m AS (
  SELECT substr(o.order_date, 1, 7) AS month, sum(o.qty * p.unit_price) AS revenue
  FROM orders o JOIN products p ON p.product_id = o.product_id
  WHERE o.status = 'Delivered'
  GROUP BY month
)
SELECT month, revenue,
       round(100.0 * (revenue - lag(revenue) OVER (ORDER BY month)) / lag(revenue) OVER (ORDER BY month), 1) AS growth_pct
FROM m ORDER BY month;

-- name: q5_jan_not_feb
-- Q5. Customers who ordered in January but not in February
SELECT count(DISTINCT customer_id) AS jan_not_feb
FROM orders o
WHERE order_date BETWEEN '2026-01-01' AND '2026-01-31'
  AND NOT EXISTS (SELECT 1 FROM orders f
                  WHERE f.customer_id = o.customer_id
                    AND f.order_date BETWEEN '2026-02-01' AND '2026-02-28');
