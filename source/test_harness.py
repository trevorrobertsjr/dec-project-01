from us_real_estate.connectors.us_real_estate import UsRealEstateApiClient
from us_real_estate.connectors.postgres import PostgreSqlClient
from sqlalchemy import Table, Column, Integer, String, MetaData, Float, DateTime
from dotenv import load_dotenv
import os
import pandas as pd

def csvout(df):
    filename = "harnessoutput.csv"
    # Check if the CSV file already exists
    file_exists = os.path.isfile(f"./output-data/csv/{filename}")

    if file_exists:
        # If file exists, append without header
        df.to_csv(f"./output-data/csv/{filename}", mode='a', header=False, index=False)
    else:
        # If file doesn't exist, create and write with header
        df.to_csv(f"./output-data/csv/{filename}", mode='w', header=True, index=False)

def sqlout(df,postgresql_client, table, metadata):
    postgresql_client.write_to_table(df.to_dict(orient="records"), table, metadata)


def main():
    filename = "harnessoutput.csv"
    if os.path.isfile(f"./output-data/csv/{filename}"):
        os.remove(f"./output-data/csv/{filename}")


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
    "us_real_estate_harness", metadata,
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
    # zip_code_list = pd.read_csv("input-data/zipcodes.csv", dtype={'zipcodes': 'str'}, header=0)['zipcodes'].tolist()
    zip_code_list=["02108", "02115"]


    for zipcode in zip_code_list:
        df = us_real_estate_client.get_listings(zipcode)
        csvout(df)
        sqlout(df,postgresql_client, table, metadata)


if __name__ == "__main__":
    main()
    