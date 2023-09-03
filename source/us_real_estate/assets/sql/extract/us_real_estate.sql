{% set config = {
    "extract_type": "incremental", 
    "incremental_column": "date_collected",
    "source_table_name": "us_real_estate_listings"
} %}

select 
    permalink,
    list_price,
    list_date,
    description_sold_date,
    location_address_postal_code,
    location_county_name,
    location_address_city,
    location_address_state,
    description_sqft,
    description_lot_sqft,
    date_collected
from 
    {{ config["source_table_name"] }}

{% if is_incremental %}
    where {{ config["incremental_column"] }} > '{{ incremental_value }}'
{% endif %}
