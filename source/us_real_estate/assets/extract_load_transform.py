import pandas as pd
from jinja2 import Environment
from graphlib import TopologicalSorter
from us_real_estate.assets.database_extractor import SqlExtractParser, DatabaseTableExtractor
# from us_real_estate.connectors.us_real_estate import UsRealEstateApiClient
from us_real_estate.connectors.postgres import PostgreSqlClient
from sqlalchemy import Table, Column, Integer, String, MetaData, Float, DateTime

def transform():
    pass

def raw_load(us_real_estate_client, raw_database_client):
    if raw_database_client.table_exists("us_real_estate_listings") and raw_database_client.is_raw_data_current():
        # print("Raw database is current. Next source data update happens at the monthly interval.")
        pass
    else:
        # SQL Alchemy for Raw database creation.
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
            Column('description_lot_sqft', Float),
            Column('date_collected', DateTime, nullable=False)
        )
        # Retrieve list of zipcodes.
        zip_code_list = pd.read_csv("us_real_estate/data/zipcodes-test.csv", dtype={'zipcodes': 'str'}, header=0)['zipcodes'].tolist()

        for zipcode in zip_code_list:
            # Create/Upsert each zipcode's data to the us_real_estate_listings table from the API
            df = us_real_estate_client.get_listings(zipcode)
            # Only write data to table if df has records
            if df is not None:
                raw_database_client.write_to_table(df.to_dict(orient="records"), table, metadata)

def analytics_load(template_environment: Environment, source_postgresql_client: PostgreSqlClient, target_postgresql_client: PostgreSqlClient):
    """
    Perform data extraction specified in a jinja template_environment.
    
    Data is extracted using a source_postgresql_client, and loaded using a target_postgresql_client. 
    """
    for asset in template_environment.list_templates():
        sql_extract_parser = SqlExtractParser(file_path=asset, environment=template_environment)
        database_table_extractor = DatabaseTableExtractor(
            sql_extract_parser=sql_extract_parser, 
            source_postgresql_client=source_postgresql_client,
            target_postgresql_client=target_postgresql_client
        )
        table_schema, metadata = database_table_extractor.get_table_schema()
        table_data = database_table_extractor.extract()
        target_postgresql_client.upsert_in_chunks(data=table_data, table=table_schema, metadata=metadata)

class SqlTransform:
    def __init__(self, postgresql_client: PostgreSqlClient, environment: Environment, table_name: str):
        self.postgresql_client = postgresql_client
        self.environment = environment
        self.table_name = table_name
        self.template = self.environment.get_template(f"{table_name}.sql")
        
    def create_table_as(self) -> None:
        """
        Drops the table if it exists and creates a new copy of the table using the provided select statement. 
        """
        exec_sql = f"""
            drop table if exists {self.table_name};
            create table {self.table_name} as (
                {self.template.render()}
            )
        """
        self.postgresql_client.execute_sql(exec_sql)

    def create_analytics_table(self) -> None:
        self.postgresql_client.execute_sql(self.template.render())

def transform(dag: TopologicalSorter):
    """
    Performs `create table as` on all nodes in the provided DAG. 
    """
    dag_rendered = tuple(dag.static_order())
    for node in dag_rendered: 
        node.create_analytics_table()
