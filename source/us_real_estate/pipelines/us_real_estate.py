from us_real_estate.connectors.us_real_estate import UsRealEstateApiClient
from us_real_estate.connectors.postgres import PostgreSqlClient
from us_real_estate.assets.extract_load_transform import raw_load
 

from dotenv import load_dotenv
import os
import pandas as pd

def main():
    load_dotenv()

    # retrieve credentials from environment variables
    X_RapidAPI_Key=os.environ.get("X-RapidAPI-Key")
    X_RapidAPI_Host=os.environ.get("X-RapidAPI-Host")
    RAW_DATABASE_NAME=os.environ.get("RAW_DATABASE_NAME")
    RAW_SERVER_NAME=os.environ.get("RAW_SERVER_NAME")
    RAW_USERNAME=os.environ.get("RAW_USERNAME")
    RAW_PASSWORD=os.environ.get("RAW_PASSWORD")
    RAW_PORT=os.environ.get("RAW_PORT")
    ANALYTICS_DATABASE_NAME=os.environ.get("ANALYTICS_DATABASE_NAME")
    ANALYTICS_SERVER_NAME=os.environ.get("ANALYTICS_SERVER_NAME")
    ANALYTICS_USERNAME=os.environ.get("ANALYTICS_USERNAME")
    ANALYTICS_PASSWORD=os.environ.get("ANALYTICS_PASSWORD")
    ANALYTICS_PORT=os.environ.get("ANALYTICS_PORT")

    # Connect to the US Real Estate API
    us_real_estate_client = UsRealEstateApiClient(api_key=X_RapidAPI_Key, api_host=X_RapidAPI_Host)
    # Connect to raw data zone database
    raw_database_client = PostgreSqlClient(
        server_name=RAW_SERVER_NAME,
        database_name=RAW_DATABASE_NAME,
        username=RAW_USERNAME,
        password=RAW_PASSWORD,
        port=RAW_PORT
    )
    # Connect to analytics data zone database
    analytics_database_client = PostgreSqlClient(
        server_name=ANALYTICS_SERVER_NAME,
        database_name=ANALYTICS_DATABASE_NAME,
        username=ANALYTICS_USERNAME,
        password=ANALYTICS_PASSWORD,
        port=ANALYTICS_PORT
    )

    # Create raw database with API data if it does not exist.
    raw_load(us_real_estate_client, raw_database_client)

if __name__ == "__main__":
    main()    