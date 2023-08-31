-- Description: SQL queries for the project
-- Initialize no nulls table for queries. Also changed location_address_postal_code to a string to account for leading zeros.
CREATE TABLE listings_nonull AS
SELECT
    permalink,
    list_price,
    list_date,
    description_sold_date,
    LPAD(CAST(location_address_postal_code AS VARCHAR), 5, '0') AS location_address_postal_code,
    location_county_name,
    location_address_city,
    location_address_state,
    description_sqft,
    description_lot_sqft
FROM listings
WHERE
    permalink IS NOT NULL
AND list_price IS NOT NULL
AND list_date IS NOT NULL
AND description_sold_date IS NOT NULL
AND location_address_postal_code IS NOT NULL
AND location_county_name IS NOT NULL
AND location_address_city IS NOT NULL
AND location_address_state IS NOT NULL
AND description_sqft IS NOT NULL
AND description_lot_sqft IS NOT NULL;


-- Trevor's questions
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

-- Trevor's questions
-- 2. What is the average home price in a state and how do home prices compare in the zip code that a prospective buyer is searching for homes in?
CREATE TABLE prospective_buyer AS
WITH StateAverage AS (
    SELECT
        location_address_state,
        ROUND(AVG(CAST(list_price AS numeric)),2) AS avg_state_price
    FROM listings_nonull
    GROUP BY location_address_state
),

ZipCodeAverage AS (
    SELECT
        location_address_postal_code,
        location_address_state,
        ROUND(AVG(CAST(list_price AS numeric)),2) AS avg_zip_price
    FROM listings_nonull
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

-- Trevor's questions
-- 3. What home characteristics aside from square footage appear to affect price (ex: year built, number of rooms, etc.)? Do the factors that affect price vary in different states?
--    I am not sure how to answer this with just SQL queries this is more of a machine learning question. I would need to use a regression model to determine the factors that affect price.

-- Trevor's questions
-- 4. How does price vary for homes with similar characteristics based on number of days listed (today date - list date as new column in transformed table)
--    I am not sure how to answer this as well. This is more of a machine learning problem too I think and would need to group the homes by similar characteristics and then compare the prices based on the number of days listed. I think this could be a good k-means clustering problem.



-- Max's questions
-- 1. How many sold homes are in each zip code?
CREATE TABLE sold_homes_per_zip AS
SELECT
    location_address_postal_code AS zip_code,
    COUNT(*) AS home_count
FROM listings_nonull
GROUP BY location_address_postal_code
ORDER BY home_count DESC, zip_code;

-- Max's questions
-- 2. 10 most expensive homes/across all zip codes

-- Alternate 1
-- The top 10 most expensive homes regardless of zip code
CREATE TABLE most_expensive_top_10_per_zip AS
SELECT
    permalink,
    list_price,
    location_address_postal_code AS zip_code,
    location_address_city AS city,
    location_address_state AS state
FROM listings_nonull
ORDER BY list_price DESC
LIMIT 10;

-- Alternate 2
-- The top 10 most expensive homes per zip code
CREATE TABLE most_expensive_top_10_per_zip AS
WITH RankedHomes AS (
    SELECT
        permalink,
        list_price,
        location_address_postal_code AS zip_code,
        location_address_city AS city,
        location_address_state AS state,
        ROW_NUMBER() OVER(PARTITION BY location_address_postal_code ORDER BY list_price DESC) AS rn
    FROM listings_nonull
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

-- Max's questions
-- 3. How long it took to sell the biggest homes per zip code
-- ***Note: I had to include the CASE statement to account for the fact that some homes were sold before they were listed.
-- I think this is a data input issue. I am also not sure if this is the best way to handle this issue.***
CREATE TABLE AS biggest_homes_listing_time AS
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
    FROM listings_nonull
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



-- Max's questions
-- 4. Longest days on the market by home size
-- ***Note: I had to include the ABS() statement to account for the fact that some homes were sold before they were listed (times were negative).
CREATE TABLE longest_days_home_size AS
SELECT
    permalink,
    description_sqft AS home_size,
    list_date,
    description_sold_date,
    ABS(EXTRACT(DAY FROM (description_sold_date - list_date))) AS days_on_market
FROM listings_nonull
ORDER BY description_sqft DESC, days_on_market DESC;

-- Max's questions
-- 5. When the most expensive homes were sold and where

CREATE TABLE when_most_expensive_homes_sold AS
SELECT
    permalink,
    list_price,
    description_sold_date AS sold_date,
    location_address_city AS city,
    location_address_state AS state,
    location_address_postal_code AS zip_code
FROM listings_nonull
ORDER BY list_price DESC, description_sold_date DESC;

-- Max's questions
-- 6. Most expensive homes sold before during and after covid
-- Not sure how to answer this question. I would need to know the dates of covid and then compare the sold dates to those dates. I would also need to know the dates of covid in each state and compare the sold dates to those dates.

-- Max's questions
-- 7. Average home price of top 10 most expensive homes sold before and after covid
-- Not sure how to answer this question. I would need to know the dates of covid and then compare the sold dates to those dates. I would also need to know the dates of covid in each state and compare the sold dates to those dates.

-- Max's questions
-- 8. Location of most expensive homes sold before, during after covid.
-- Not sure how to answer this question. I would need to know the dates of covid and then compare the sold dates to those dates. I would also need to know the dates of covid in each state and compare the sold dates to those dates.