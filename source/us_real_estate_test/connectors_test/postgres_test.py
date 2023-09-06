from us_real_estate.connectors.postgres import PostgreSqlClient
from sqlalchemy import Table, Column, Integer, String, MetaData
from dotenv import load_dotenv
import os
import pytest


@pytest.fixture
def setup_postgresql_client():
    load_dotenv()
    RAW_SERVER_NAME = os.environ.get("RAW_SERVER_NAME")
    RAW_DATABASE_NAME = os.environ.get("RAW_DATABASE_NAME")
    RAW_USERNAME = os.environ.get("RAW_USERNAME")
    RAW_PASSWORD = os.environ.get("RAW_PASSWORD")
    RAW_PORT = os.environ.get("RAW_PORT")

    postgresql_client = PostgreSqlClient(
        server_name=RAW_SERVER_NAME,
        database_name=RAW_DATABASE_NAME,
        username=RAW_USERNAME,
        password=RAW_PASSWORD,
        port=RAW_PORT
    ) 
    return postgresql_client

@pytest.fixture
def setup_table():
    table_name = "Unit_test_table"
    metadata = MetaData()
    table = Table(
        table_name,
        metadata,
        Column("house_id", Integer, primary_key=True),
        Column("house_value", Integer),
        Column("state_name", String)
    )
    return table_name, table, metadata
def test_postgresql_client_insert(setup_postgresql_client, setup_table):
    postgresql_client = setup_postgresql_client
    table_name, table, metadata = setup_table
    postgresql_client.drop_table(table_name) # make sure any testing tables will not remain in the database.

    #Creating some data within the testing table
    test_data = [
        {"house_id": "00256", "house_value": "$450000", "state_name": "Texas"},
        {"house_id": "00385", "house_value": "$650000", "state_name": "Nevada"},
        {"house_id": "00856", "house_value": "$850000", "state_name": "New York"}

    ]
    # Calling the function to test. (ACT)
    postgresql_client.insert(data=test_data, table=table_name, metadata=metadata)

    result = postgresql_client.select_all(table=table_name)

    assert len(result) == 3

    postgresql_client.drop_table(table_name) # dropping unnecessary/additional tables after testing
