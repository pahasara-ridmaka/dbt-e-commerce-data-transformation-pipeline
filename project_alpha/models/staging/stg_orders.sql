WITH source AS (
    SELECT * FROM read_csv_auto('../data/raw/orders.csv')
),

removed_duplicates AS (
    SELECT *
    FROM source
    QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY order_date DESC) = 1
),

cleaned AS (
    SELECT DISTINCT
        order_id,
        user_id,
        product_id,
        CAST(order_date AS DATE) AS order_date,
        CAST(quantity AS INTEGER) AS quantity,
    FROM removed_duplicates
    WHERE order_id IS NOT NULL
)

SELECT * FROM cleaned