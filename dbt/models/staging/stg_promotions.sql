WITH source AS (
    SELECT * FROM read_csv_auto('../data/raw/promotions.csv')
),

cleaned AS (
    SELECT
        promo_id AS promotion_id,
        UPPER(TRIM(promo_code)) AS promotion_code,
        discount_pct AS discount_percentage,
    FROM source
    WHERE promotion_id IS NOT NULL
)


SELECT * FROM cleaned