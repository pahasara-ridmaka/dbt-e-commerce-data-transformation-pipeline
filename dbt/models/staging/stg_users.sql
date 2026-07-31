WITH source AS (
  SELECT * FROM read_csv_auto('../data/raw/users.csv')
),

cleaned AS (

  SELECT
    user_id,
    CASE
      WHEN LOWER(TRIM(full_name)) = 'n/a' THEN 'NULL'
      ELSE LOWER(TRIM(full_name))
    END AS full_name,
    CASE
      WHEN LOWER(TRIM(email)) is NULL OR LOWER(TRIM(email)) = 'n/a' THEN 'NULL'
      ELSE LOWER(TRIM(email))
    END AS email,
    CAST(signup_date AS DATE) AS signup_date,
    LOWER(region) AS region
  FROM source
  WHERE user_id IS NOT NULL
)


SELECT * FROM cleaned








