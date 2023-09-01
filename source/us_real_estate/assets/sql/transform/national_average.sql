-- 1. Which cities, states, regions are seeing below/above national average home prices?

CREATE TABLE national_average AS
WITH NationalAverage AS (
    SELECT AVG(CAST(list_price AS numeric)) as national_avg_price
    FROM listings_nonull
)

SELECT
    location_address_city AS city,
    location_address_state AS state,
    location_county_name AS region,
    ROUND(AVG(CAST(list_price AS numeric)), 2) AS avg_price,
    CASE
        WHEN AVG(CAST(list_price AS numeric)) > (SELECT national_avg_price FROM NationalAverage) THEN 'Above National Average'
        ELSE 'Below National Average'
    END AS comparison
FROM listings_nonull
GROUP BY location_address_city, location_address_state, location_county_name
ORDER BY location_address_state, location_address_city, location_county_name;