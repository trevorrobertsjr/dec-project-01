-- 3. How long it took to sell the biggest homes per zip code
-- ***Note: I had to include the CASE statement to account for the fact that some homes were sold before they were listed.
-- I think this is a data input issue. I am also not sure if this is the best way to handle this issue.***
CREATE TABLE biggest_homes_listing_time AS
WITH BiggestHomes AS (
    SELECT
        permalink,
        list_price,
        location_address_postal_code AS zip_code,
        location_address_city AS city,
        location_address_state AS state,
        description_sqft,
        list_date,
        description_sold_date,
        ROW_NUMBER() OVER(PARTITION BY location_address_postal_code ORDER BY description_sqft DESC, list_price DESC) AS rn
    FROM us_real_estate_listings
)

SELECT
    permalink,
    list_price,
    zip_code,
    city,
    state,
    description_sqft,
    list_date,
    description_sold_date,
    CASE
        WHEN description_sold_date - list_date < interval '0' THEN (list_date - description_sold_date)
        ELSE (description_sold_date - list_date)
    END AS time_on_market
FROM BiggestHomes
WHERE rn = 1
ORDER BY description_sqft DESC, list_price DESC;