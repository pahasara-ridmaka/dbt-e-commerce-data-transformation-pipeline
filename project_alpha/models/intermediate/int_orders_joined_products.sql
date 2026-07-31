WITH stg_orders AS (
    SELECT *
    FROM {{ref('stg_orders')}}
),
stg_products AS (
    SELECT *
    FROM {{ ref('stg_products') }}
)
SELECT
    o.order_id,
    o.user_id,
    p.product_id,
    o.order_date,
    o.quantity,
    p.price,
    (o.quantity * p.price) AS total_amount,
    p.category


FROM stg_orders o
JOIN stg_products p ON o.product_id = p.product_id


