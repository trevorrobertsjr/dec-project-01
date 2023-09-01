-- 4. Longest days on the market by home size
-- ***Note: I had to include the ABS() statement to account for the fact that some homes were sold before they were listed (times were negative).
CREATE TABLE longest_days_home_size AS
SELECT
    permalink,
    description_sqft AS home_size,
    list_date,
    description_sold_date,
    ABS(EXTRACT(DAY FROM (description_sold_date - list_date))) AS days_on_market
FROM us_real_estate_listings
ORDER BY description_sqft DESC, days_on_market DESC;