
WITH product AS (
    SELECT *
    FROM {{ ref('stg_products') }}
)


SELECT
    product_id,
    product_name,
    category,
    stock_level,
    CASE
        WHEN stock_level < 10 THEN 'Low Stock'
        ELSE 'In Stock'
    END AS inventory_status

FROM product 