from us_real_estate.connectors.us_real_estate import UsRealEstateApiClient
from us_real_estate.connectors.postgres import PostgreSqlClient
from us_real_estate.assets.us_real_estate import extract, load 
from sqlalchemy import Table, Column, Integer, String, MetaData, Float, DateTime
from dotenv import load_dotenv
import os
import pandas as pd

def main():
    load_dotenv()
    X_RapidAPI_Key=os.environ.get("X-RapidAPI-Key")
    X_RapidAPI_Host=os.environ.get("X-RapidAPI-Host")

    # Connect to raw data zone database
    RAW_DATABASE_NAME=os.environ.get("RAW_DATABASE_NAME")
    RAW_SERVER_NAME=os.environ.get("RAW_SERVER_NAME")
    RAW_USERNAME=os.environ.get("RAW_USERNAME")
    RAW_PASSWORD=os.environ.get("RAW_PASSWORD")
    RAW_PORT=os.environ.get("RAW_PORT")
    us_real_estate_client = UsRealEstateApiClient(api_key=X_RapidAPI_Key, api_host=X_RapidAPI_Host)
    postgresql_client = PostgreSqlClient(
        server_name=RAW_SERVER_NAME,
        database_name=RAW_DATABASE_NAME,
        username=RAW_USERNAME,
        password=RAW_PASSWORD,
        port=RAW_PORT
    )
    metadata = MetaData()
    table = Table(
    "us_real_estate_listings", metadata,
        Column('permalink', String, primary_key=True),
        Column('list_price', String),
        Column('list_date', DateTime, primary_key=True),
        Column('description_sold_date', DateTime),
        Column('location_address_postal_code', Integer),
        Column('location_county_name', String),
        Column('location_address_city', String),
        Column('location_address_state', String),
        Column('description_sqft', Float),
        Column('description_lot_sqft', Float)
    )
    
    #This turns the column into a string and keeps the leading zeros.
    zip_code_list = pd.read_csv("us_real_estate/data/zipcodes-test.csv", dtype={'zipcodes': 'str'}, header=0)['zipcodes'].tolist()

    for zipcode in zip_code_list:
        df = extract(us_real_estate_client, zipcode)
        # Only attempt to load data to the database if this iteration's extract succeeds
        if df is not None:
            load(df,postgresql_client, table, metadata)

if __name__ == "__main__":
    main()    