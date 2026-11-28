-- Best month for every store: ROW_NUMBER inside a CTE, then keep row 1
WITH ranked AS (
    SELECT store, month, revenue,
           ROW_NUMBER() OVER (PARTITION BY store ORDER BY revenue DESC) AS rn
    FROM monthly_sales
)
SELECT store, month, revenue FROM ranked WHERE rn = 1 ORDER BY revenue DESC;
