-- Month-on-month change for one store, with LAG
SELECT month, revenue,
       LAG(revenue) OVER (PARTITION BY store ORDER BY month) AS prev_month,
       revenue - LAG(revenue) OVER (PARTITION BY store ORDER BY month) AS change
FROM monthly_sales
WHERE store = 'Kochi-1';
