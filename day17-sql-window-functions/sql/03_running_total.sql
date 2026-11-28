-- Running total and 3-month moving average for one store
SELECT month, revenue,
       SUM(revenue) OVER (PARTITION BY store ORDER BY month) AS running_total,
       CAST(ROUND(AVG(revenue) OVER (PARTITION BY store ORDER BY month
             ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)) AS INTEGER) AS avg_3m
FROM monthly_sales
WHERE store = 'Kochi-1';
