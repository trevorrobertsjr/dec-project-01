from us_real_estate.connectors.us_real_estate import UsRealEstateApiClient
from us_real_estate.connectors.postgres import PostgreSqlClient
from sqlalchemy import Table, Column, Integer, String, MetaData, Float, DateTime
from dotenv import load_dotenv
import os
import pandas as pd

# Create/Upsert each zipcode's data to the us_real_estate_listings table from the API
def extract(us_real_estate_client, zipcode):
    return us_real_estate_client.get_listings(zipcode)

def load(df,postgresql_client, table, metadata):
    postgresql_client.write_to_table(df.to_dict(orient="records"), table, metadata)

def transform():
    pass