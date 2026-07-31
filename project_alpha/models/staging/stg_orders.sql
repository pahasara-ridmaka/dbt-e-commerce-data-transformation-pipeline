WITH source AS (
    SELECT * FROM read_csv_auto('../data/raw/orders.csv')
),

cleaned AS (
    SELECT
        order_id,
        user_id,
        product_id,
        CAST(order_date AS DATE) AS order_date,
        CAST(quantity AS INTEGER) AS quantity,
    FROM source
    WHERE order_id IS NOT NULL
)

SELECT * FROM cleaned