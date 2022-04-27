
# TODO: See if you can narrow the scope of the columns (e.g. VARCHAR -> VARCHAR(50) or whatever.) 

# ----------------------- SCRIPT ------------------------------------------------------

import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events CASCADE;"
staging_songs_table_drop = ""
songplay_table_drop = ""
user_table_drop = ""
song_table_drop = ""
artist_table_drop = ""
time_table_drop = ""

# Note: Do not bother with Forgein Keys' as AWS does not enforce them and counts on your own 
#       ETL to enforce them, it does however enforce 'NOT NULL'. I will still define a PK just
#       to make it clearer for me and the reader.

# CREATE TABLES
staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_events(
    id IDENTITY(0,1) NOT NULL,
    auth VARCHAR(50) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    gender VARCHAR(5),
    location VARCHAR,
    user_id INT NOT NULL, 
    artist VARCHAR(255),
    song VARCHAR(255), 
    length FLOAT,
    level VARCHAR(50),
    session_id INT,
    item_in_session INT(255),
    page VARCHAR(50), 
    method VARCHAR(10),
    status INT(3)
    user_agent VARCHAR,
    registration BIGINT,
    ts TIMESTAMP
    PRIMARY KEY (id));
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs(
    id IDENTITY(0,1) NOT NULL,
    artist_id VARCHAR,
    artist_latitude FlOAT,
    artist_longitute FLOAT,
    artist_name VARCHAR,
    duration FLOAT,
    song_id VARCHAR,
    title VARCHAR,
    year INTEGER
    PRIMARY KEY (id));
""")

songplay_table_create = ("""
    // Double check if these need to be 'Not Null' or not
    id IDENTITYT(0,1) NOT NULL,
    songplay_id INTEGER NOT NULL,
    start_time TIMESTAMP NOT NULL,
    user_id INTEGER NOT NULL,
    level VARCHAR(50) NOT NULL,
    song_id INTEGER NOT NULL,
    artist_id INTEGER NOT NULL,
    session_id INTEGER NOT NULL,
    location VARCHAR NOT NULL,
    user_agent VARCHAR NOT NULL,
    PRIMARY KEY (id));
""")

user_table_create = ("""
    id IDENTITYT(0,1) NOT NULL,
    user_id INTEGER NOT NULL,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    gender VARCHAR(5) ,
    level VARCHAR(50),
    PRIMARY KEY (id));    
""")

song_table_create = ("""
    id IDENTITYT(0,1) NOT NULL,
    song_id INTEGER,
    title VARCHAR,
    artist_id INTEGER,
    year INTEGER,
    duration FLOAT,
    PRIMARY KEY (id));
""")

artist_table_create = ("""
    id INDENTITYT(0,1) NOT NULL,
    artist_id VARCHAR NOT NULL,
    name VARCHAR,
    location VARCHAR,
    lattitude FLOAT,
    longitude FLOAT,
    PRIMARY KEY (id));
""")

time_table_create = ("""
    id IDENTITYT(0,1) NOT NULL,
    start_time TIMESTAMP,
    hour INTEGER,
    day VARCHAR,
    week INTEGER,
    month VARCHAR,
    year INTEGER,
    weekday VARCHAR,
    PRIMARY KEY (id));
""")

# STAGING TABLES
# We want to insert the databatches into the stagign tables from the S3 buckets
staging_events_copy = ("""
    COPY staging_events FROM '{}'
    credentials 'aws_iam_role={}'
    region 'us-west-2';
""").format(config["S3"]["LOG_DATA"], config["IAM_ROLE"]["ARN"])

staging_songs_copy = ("""
""").format()

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
