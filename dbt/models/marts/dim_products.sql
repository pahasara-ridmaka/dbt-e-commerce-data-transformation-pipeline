WITH product_inventory AS (
    SELECT *
    FROM {{ ref('int_product_inventory_status') }}
)


SELECT * FROM product_inventory