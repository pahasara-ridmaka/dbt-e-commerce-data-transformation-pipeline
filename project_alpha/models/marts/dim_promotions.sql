WITH stg_promotions AS (
    SELECT * 
    FROM {{ ref('stg_promotions') }}
)

SELECT * FROM stg_promotions