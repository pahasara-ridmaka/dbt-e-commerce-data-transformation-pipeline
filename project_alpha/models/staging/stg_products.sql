WITH source AS (
    SELECT * FROM read_csv_auto('../data/raw/products.csv')
),

cleaned AS (
    SELECT
        product_id,
        LOWER(TRIM(product_name)) AS product_name,
        CASE
            WHEN LOWER(TRIM(category)) = 'elec' THEN 'electronics'
            ELSE LOWER(TRIM(category))
        END AS category,
        CASE
            WHEN CAST(price AS FLOAT) IS NULL OR CAST(price AS FLOAT) < 0 THEN 100
            ELSE CAST(price AS FLOAT)
        END AS price,
        CAST(stock_level AS INT) AS stock_level

    FROM source
    WHERE product_id IS NOT NULL
)


SELECT * FROM cleaned