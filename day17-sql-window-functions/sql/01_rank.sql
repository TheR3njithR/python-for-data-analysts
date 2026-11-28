-- June 2026: rank the stores by revenue, three ways
SELECT store, revenue,
       RANK()       OVER (ORDER BY revenue DESC) AS rnk,
       DENSE_RANK() OVER (ORDER BY revenue DESC) AS dense_rnk,
       ROW_NUMBER() OVER (ORDER BY revenue DESC, store) AS row_num
FROM monthly_sales
WHERE month = '2026-06';
