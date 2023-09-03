DROP TABLE IF EXISTS most_expensive_top_10_per_zip;
CREATE TABLE most_expensive_top_10_per_zip AS
WITH RankedHomes AS (
    SELECT
        permalink,
        list_price,
        location_address_postal_code AS zip_code,
        location_address_city AS city,
        location_address_state AS state,
        ROW_NUMBER() OVER(PARTITION BY location_address_postal_code ORDER BY list_price DESC) AS rn
    FROM us_real_estate_listings
)
SELECT
    permalink,
    list_price,
    zip_code,
    city,
    state
FROM RankedHomes
WHERE rn = 1
ORDER BY list_price desc
limit 10;