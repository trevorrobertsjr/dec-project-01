DROP TABLE IF EXISTS sold_homes_per_zip;
CREATE TABLE sold_homes_per_zip AS
SELECT
    location_address_postal_code AS zip_code,
    COUNT(*) AS home_count
FROM us_real_estate_listings
GROUP BY location_address_postal_code
ORDER BY home_count DESC, zip_code;