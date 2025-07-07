import yaml
from sqlalchemy import create_engine
import psycopg2

with open("../config.yaml", "r") as file:
    CONFIG = yaml.safe_load(file)

DB_CONFIG = {
    'host': CONFIG.get('db_host'),
    'database': CONFIG.get('db_name'),
    'user': CONFIG.get('db_user'),
    'password': CONFIG.get('db_password'),
    'port': CONFIG.get('db_port', 5432)
}

def connect_to_database():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn.cursor()
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def get_engine():
    db_url = (
        f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    return create_engine(db_url)

def save_to_postgis(gdf, table_name, schema, if_exists):
    engine = get_engine()
    gdf.to_postgis(table_name, engine, schema=schema, if_exists=if_exists)
    print(f"Data saved to '{schema}.{table_name}' in database '{DB_CONFIG['database']}'.")
