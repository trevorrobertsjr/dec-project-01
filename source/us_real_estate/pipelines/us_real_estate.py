from dotenv import load_dotenv
import os
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from graphlib import TopologicalSorter
from us_real_estate.connectors.us_real_estate import UsRealEstateApiClient
from us_real_estate.connectors.postgres import PostgreSqlClient
from us_real_estate.assets.extract_load_transform import raw_load, analytics_load, transform, SqlTransform
from us_real_estate.assets.pipeline_logging import PipelineLogging
from us_real_estate.assets.metadata_logging import MetaDataLogging, MetaDataLoggingStatus


def main():
    load_dotenv()
    # retrieve logging database credentials
    LOGGING_SERVER_NAME = os.environ.get("LOGGING_SERVER_NAME")
    LOGGING_DATABASE_NAME = os.environ.get("LOGGING_DATABASE_NAME")
    LOGGING_USERNAME = os.environ.get("LOGGING_USERNAME")
    LOGGING_PASSWORD = os.environ.get("LOGGING_PASSWORD")
    LOGGING_PORT = os.environ.get("LOGGING_PORT")

    # connect to logging database
    postgresql_logging_client = PostgreSqlClient(
        server_name=LOGGING_SERVER_NAME,
        database_name=LOGGING_DATABASE_NAME,
        username=LOGGING_USERNAME,
        password=LOGGING_PASSWORD,
        port=LOGGING_PORT
    )

    metadata_logging = MetaDataLogging(pipeline_name="us_real_estate", postgresql_client=postgresql_logging_client)
    pipeline_logging = PipelineLogging(pipeline_name="us_real_estate", log_folder_path="us_real_estate/logs")

    # retrieve api, raw database, and analytics database credentials from environment variables
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
    try:
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
        raw_load_status = raw_load(us_real_estate_client, raw_database_client)
        if raw_load_status:
            pipeline_logging.logger.info(raw_load_status)
        else:
            pipeline_logging.logger.info("Perform raw database build and load")

        analytics_template_environment = Environment(loader=FileSystemLoader("us_real_estate/assets/sql/extract"))
        pipeline_logging.logger.info("Perform analytics database build and load")
        analytics_load(
            template_environment=analytics_template_environment, 
            source_postgresql_client=raw_database_client, 
            target_postgresql_client=analytics_database_client
        )
        transform_template_environment = Environment(loader=FileSystemLoader("us_real_estate/assets/sql/transform"))
        
        # create nodes
        biggest_homes_listing_time = SqlTransform(table_name="biggest_homes_listing_time", postgresql_client=analytics_database_client, environment=transform_template_environment)
        longest_days_home_size = SqlTransform(table_name="longest_days_home_size", postgresql_client=analytics_database_client, environment=transform_template_environment)
        most_expensive_top_10_per_zip = SqlTransform(table_name="most_expensive_top_10_per_zip", postgresql_client=analytics_database_client, environment=transform_template_environment)
        national_average = SqlTransform(table_name="national_average", postgresql_client=analytics_database_client, environment=transform_template_environment)
        prospective_buyer = SqlTransform(table_name="prospective_buyer", postgresql_client=analytics_database_client, environment=transform_template_environment)
        sold_homes_per_zip = SqlTransform(table_name="sold_homes_per_zip", postgresql_client=analytics_database_client, environment=transform_template_environment)
        when_most_expensive_homes_sold = SqlTransform(table_name="when_most_expensive_homes_sold", postgresql_client=analytics_database_client, environment=transform_template_environment)
        
        # create DAG 
        dag = TopologicalSorter()
        dag.add(biggest_homes_listing_time)
        dag.add(longest_days_home_size)
        dag.add(most_expensive_top_10_per_zip)
        dag.add(national_average)
        dag.add(prospective_buyer)
        dag.add(sold_homes_per_zip)
        dag.add(when_most_expensive_homes_sold)
        # run transform 
        pipeline_logging.logger.info("Perform transform")
        transform(dag=dag)
        pipeline_logging.logger.info("Pipeline complete")
        metadata_logging.log(status=MetaDataLoggingStatus.RUN_SUCCESS, logs=pipeline_logging.get_logs()) 
        pipeline_logging.logger.handlers.clear()

    except BaseException as e:
        pipeline_logging.logger.error(f"Pipeline failed with exception {e}")
        metadata_logging.log(status=MetaDataLoggingStatus.RUN_FAILURE, logs=pipeline_logging.get_logs()) 
        pipeline_logging.logger.handlers.clear()

if __name__ == "__main__":
    main()    