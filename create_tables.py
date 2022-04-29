
# TODO: Make redshift cluster with script 
import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries

# --- CONFIG ----
config = configparser.ConfigParser()
config.read_file(open('dwh.cfg'))

DWH_CLUSTER_IDENTIFIER= config.get("CLUSTER","DWH_CLUSTER_IDENTIFIER")
DWH_DB                = config.get("CLUSTER","DB_NAME")
DWH_DB_USER           = config.get("CLUSTER","DB_USER")
DWH_DB_PASSWORD       = config.get("CLUSTER","DB_PASSWORD")
DWH_PORT              = config.get("CLUSTER","DB_PORT")
DWH_ENDPOINT          = config.get("CLUSTER", "DWH_ENDPOINT")



def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn_string="postgresql://{}:{}@{}:{}/{}".format(DWH_DB_USER, DWH_DB_PASSWORD, DWH_ENDPOINT, DWH_PORT,DWH_DB)
    conn = psycopg2.connect(conn_string)    
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
