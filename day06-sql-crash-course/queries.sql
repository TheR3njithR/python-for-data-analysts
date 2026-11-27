-- name: q0_look
-- First look: every column, first 5 rows
SELECT * FROM orders LIMIT 5;

-- name: q1_where
-- 1. SELECT + WHERE: delivered orders in October 2026 with 3 or more items
SELECT order_id, order_date, qty, status
FROM orders
WHERE status = 'Delivered' AND order_date >= '2026-10-01' AND qty >= 3
ORDER BY order_date
LIMIT 5;

-- name: q1_where_count
SELECT count(*) AS orders FROM orders
WHERE status = 'Delivered' AND order_date >= '2026-10-01' AND qty >= 3;

-- name: q2_order_by
-- 2. ORDER BY + LIMIT: the five most expensive products
SELECT product_name, category, unit_price
FROM products
ORDER BY unit_price DESC
LIMIT 5;

-- name: q3_group_by
-- 3. GROUP BY: revenue and orders per category (delivered only)
SELECT p.category, count(*) AS orders, round(sum(o.qty * p.unit_price * (1 - o.discount_pct / 100))) AS revenue
FROM orders o JOIN products p ON p.product_id = o.product_id
WHERE o.status = 'Delivered'
GROUP BY p.category
ORDER BY revenue DESC;

-- name: q4_having
-- 4. HAVING: cities where the return-or-cancel rate is above 15 percent
SELECT c.city, count(*) AS orders,
       round(100.0 * sum(o.status <> 'Delivered') / count(*), 1) AS not_delivered_pct
FROM orders o JOIN customers c ON c.customer_id = o.customer_id
GROUP BY c.city
HAVING not_delivered_pct > 15
ORDER BY not_delivered_pct DESC;

-- name: q4_all_cities
SELECT c.city, count(*) AS orders,
       round(100.0 * sum(o.status <> 'Delivered') / count(*), 1) AS not_delivered_pct
FROM orders o JOIN customers c ON c.customer_id = o.customer_id
GROUP BY c.city ORDER BY not_delivered_pct DESC;

-- name: q5_join
-- 5. JOIN: revenue by customer segment and city (delivered only), top 5
SELECT c.segment, c.city, round(sum(o.qty * p.unit_price * (1 - o.discount_pct / 100))) AS revenue
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN products p ON p.product_id = o.product_id
WHERE o.status = 'Delivered'
GROUP BY c.segment, c.city
ORDER BY revenue DESC
LIMIT 5;

-- name: q6_left_join
-- Bonus: LEFT JOIN to find customers who never ordered
SELECT count(*) AS never_ordered
FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL;
