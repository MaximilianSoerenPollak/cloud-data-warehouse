
# TODO: See if you can narrow the scope of the columns (e.g. VARCHAR -> VARCHAR(50) or whatever.) 

# ----------------------- SCRIPT ------------------------------------------------------

import configparser
from aws_startup import iam, DWH_IAM_ROLE_NAME
# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# GET iam ROLE ARN 

rolearn = iam.get_role(RoleName=DWH_IAM_ROLE_NAME)['Role']['Arn']

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events CASCADE;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs CASCADE;"
songplay_table_drop = "DROP TABLE IF EXISTS songplay CASCADE;"
user_table_drop = "DROP TABLE IF EXISTS users CASCADE;"
song_table_drop = "DROP TABLE IF EXISTS songs CASCADE;"
artist_table_drop = "DROP TABLE IF EXISTS artists CASCADE;"
time_table_drop = "DROP TABLE IF EXISTS times CASCADE;"

# Note: Do not bother with Forgein Keys' as AWS does not enforce them and counts on your own 
#       ETL to enforce them, it does however enforce 'NOT NULL'. I will still define a PK just
#       to make it clearer for me and the reader.

# CREATE TABLES
staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_events(
    id BIGINT IDENTITY(0,1) NOT NULL,
    artist VARCHAR,
    auth VARCHAR,
    first_name VARCHAR,
    gender VARCHAR,
    item_in_session INTEGER,
    last_name VARCHAR,
    length FLOAT,
    level VARCHAR,
    location VARCHAR(500),
    method VARCHAR,
    page VARCHAR, 
    registration BIGINT,
    session_id INTEGER,
    song VARCHAR, 
    status SMALLINT,
    ts BIGINT,
    user_agent VARCHAR,
    user_id INTEGER); 
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs(
    id BIGINT IDENTITY(0,1) NOT NULL,
    artist_id VARCHAR,
    artist_latitude FlOAT,
    artist_longitude FLOAT,
    artist_name VARCHAR(500),
    duration FLOAT,
    song_id VARCHAR,
    title VARCHAR(500),
    year INTEGER);
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplay(
    id BIGINT IDENTITY(0,1) NOT NULL,
    songplay_id INTEGER,
    start_time TIMESTAMP,
    user_id INTEGER,
    level VARCHAR,
    song_id INTEGER,
    artist_id INTEGER,
    session_id INTEGER,
    location VARCHAR,
    user_agent VARCHAR);
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users(
    id BIGINT IDENTITY(0,1) NOT NULL,
    user_id INTEGER,
    first_name VARCHAR,
    last_name VARCHAR,
    gender VARCHAR,
    level VARCHAR);
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs(
    id BIGINT IDENTITY(0,1) NOT NULL,
    song_id INTEGER,
    title VARCHAR,
    artist_id INTEGER,
    year INTEGER,
    duration FLOAT);
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists(
    id BIGINT IDENTITY(0,1) NOT NULL,
    artist_id VARCHAR,
    name VARCHAR,
    location VARCHAR(500),
    lattitude FLOAT,
    longitude FLOAT);
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS times(
    id BIGINT IDENTITY(0,1) NOT NULL,
    start_time TIMESTAMP,
    hour INTEGER,
    day VARCHAR,
    week INTEGER,
    month VARCHAR,
    year INTEGER,
    weekday VARCHAR);
""")

# STAGING TABLES
# We want to insert the databatches into the stagign tables from the S3 buckets
staging_events_copy = ("""
    COPY staging_events
    FROM {}
    iam_role '{}'
    format as JSON {}
    region 'us-west-2';""").format(config["S3"]["LOG_DATA"], rolearn, config["S3"]["LOG_JSONPATH"])
staging_songs_copy = ("""
    COPY staging_songs(artist_id, artist_latitude,artist_longitude, artist_name, duration, song_id, title, year) 
    FROM {}
    iam_role '{}'
    format as JSON 'auto'
    region 'us-west-2';""").format(config["S3"]["SONG_DATA"], rolearn)

# FINAL TABLES

songplay_table_insert = ("""
    
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
