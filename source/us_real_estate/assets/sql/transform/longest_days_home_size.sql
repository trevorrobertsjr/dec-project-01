DROP TABLE IF EXISTS longest_days_home_size;
CREATE TABLE longest_days_home_size AS
SELECT
    permalink,
    description_sqft AS home_size,
    list_date,
    description_sold_date,
    ABS(EXTRACT(DAY FROM (description_sold_date - list_date))) AS days_on_market
FROM us_real_estate_listings
ORDER BY description_sqft DESC, days_on_market DESC;