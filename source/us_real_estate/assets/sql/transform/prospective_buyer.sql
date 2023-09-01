CREATE TABLE prospective_buyer AS
WITH StateAverage AS (
    SELECT
        location_address_state,
        ROUND(AVG(CAST(list_price AS numeric)),2) AS avg_state_price
    FROM us_real_estate_listings
    GROUP BY location_address_state
),

ZipCodeAverage AS (
    SELECT
        location_address_postal_code,
        location_address_state,
        ROUND(AVG(CAST(list_price AS numeric)),2) AS avg_zip_price
    FROM us_real_estate_listings
    GROUP BY location_address_postal_code, location_address_state
)

SELECT
    z.location_address_state,
    s.avg_state_price,
    z.location_address_postal_code,
    z.avg_zip_price,
    ROUND(((z.avg_zip_price - s.avg_state_price) / s.avg_state_price) * 100, 2) AS percentage_difference
FROM ZipCodeAverage z
JOIN StateAverage s ON z.location_address_state = s.location_address_state
ORDER BY z.location_address_state, z.location_address_postal_code;