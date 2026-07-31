WITH users AS (
    SELECT *
    FROM {{ ref('stg_users') }}
),
joined_orders AS (
    SELECT * 
    FROM {{ ref('int_orders_joined_products') }}
)

SELECT
    o.order_id,
    u.user_id,
    u.full_name,
    u.region,
    o.product_id,
    o.order_date,
    o.total_amount,
    o.category

FROM joined_orders o
JOIN users u ON o.user_id = u.user_id