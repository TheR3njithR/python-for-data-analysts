-- Q1: which city brings in the most revenue, and per store?
SELECT s.city,
       COUNT(DISTINCT s.store_id) AS stores,
       ROUND(SUM(o.revenue) / 100000.0, 1) AS revenue_lakh,
       ROUND(SUM(o.revenue) / 100000.0 / COUNT(DISTINCT s.store_id), 1) AS per_store_lakh
FROM orders o JOIN stores s ON s.store_id = o.store_id
GROUP BY s.city
ORDER BY revenue_lakh DESC;
