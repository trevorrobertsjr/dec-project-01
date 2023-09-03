DROP TABLE IF EXISTS when_most_expensive_homes_sold;
CREATE TABLE when_most_expensive_homes_sold AS
SELECT
    permalink,
    list_price,
    description_sold_date AS sold_date,
    location_address_city AS city,
    location_address_state AS state,
    location_address_postal_code AS zip_code
FROM us_real_estate_listings
ORDER BY list_price DESC, description_sold_date DESC;