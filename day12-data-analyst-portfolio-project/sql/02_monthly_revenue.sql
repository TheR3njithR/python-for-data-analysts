-- Q2: how does revenue move month by month?
SELECT substr(order_date, 1, 7) AS month, ROUND(SUM(revenue) / 100000.0, 1) AS revenue_lakh
FROM orders GROUP BY month ORDER BY month;
