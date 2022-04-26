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

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_events(
    id IDENTITY(0,1) NOT NULL,
    auth VARCHAR(50) NOT NULL,
    firstName VARCHAR(255),
    lastName VARCHAR(255),
    gender VARCHAR(5),
    location VARCHAR,
    userid INT NOT NULL, 
    artist VARCHAR(255),
    song VARCHAR(255), 
    length FLOAT,
    level VARCHAR(50),
    sessionID INT,
    itemInSession INT(255),
    page VARCHAR(50), 
    method VARCHAR(10),
    status INT(3)
    userAgent VARCHAR,
    registration BIGINT,
    ts TIMESTAMP);
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs(
    ID IDENTITY(0,1) NOT NULL,
    artistID VARCHAR,
    artistLatitude FlOAT,
    artistLongitute FLOAT,
    artistName VARCHAR,
    duration FLOAT,
    songID VARCHAR,
    title VARCHAR,
    year INTEGER
    );


""")

songplay_table_create = ("""
""")

user_table_create = ("""
""")

song_table_create = ("""
""")

artist_table_create = ("""
""")

time_table_create = ("""
""")

# STAGING TABLES

staging_events_copy = ("""
""").format()

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
