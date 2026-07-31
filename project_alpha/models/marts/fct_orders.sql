WITH orders_enriched AS (
    SELECT * FROM {{ ref('int_orders_enriched') }}
)

SELECT * FROM orders_enriched