from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Float
from sqlalchemy.engine import URL, Engine
from sqlalchemy.dialects import postgresql
import pandas as pd

#Create a Connection to the the Raw Database
def Raw_DB_Engine_Connection(db_user: str, db_password: str, db_server_name: str, db_database_name: str):
    # create connection to database 
    Raw_DB_Connecting_url = URL.create(
        Raw_DB_drivername = "postgresql+pg8000", 
        RAW_USERNAME = db_user,
        RAW_PASSWORD = db_password,
        RAW_SERVER_NAME = db_server_name, 
        RAW_PORT = 5432,
        RAW_DATABASE_NAME = db_database_name, 
    )

    raw_db_engine = create_engine(Raw_DB_Connecting_url)
    return raw_db_engine 

def write_to_RawDB(raw_db_engine: Engine, us_real_estate: pd.DataFrame): # information to complete once having dataset view
    meta = MetaData()
    us_real_estate_listing = Table(
        "real_estate_listing", meta, 
        Column("", Integer, primary_key=True),
        Column("", String, ),
        Column("", String, ),
        Column("", Float),
        Column("", Integer),
        Column("", Integer),       # variable type to be modified based on Data type from the Dataset
        Column("", Float),   
    )
    meta.create_all(raw_db_engine) # generate new table if they do not exist
    key_columns = [pk_column.name for pk_column in us_real_estate_listing.primary_key.columns.values()]
    insert_statement = postgresql.insert(us_real_estate_listing).values(us_real_estate.to_dict(orient='records'))
    # # upsert_statement = insert_statement.on_conflict_do_update(
    # #     index_elements=key_columns,
    #     set_={c.key: c for c in insert_statement.excluded if c.key not in key_columns})
    
# raw_db_engine.execute(upsert_statement)
# Upsert statement to test when data is ready