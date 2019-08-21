# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplay;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""
    CREATE TABLE songplays (
        songplay_id int,
        start_time timestamp,
        user_id int,
        level varchar,
        song_id varchar,
        artist_id varchar,
        session_id int,
        location varchar,
        user_agent varchar
    );
""")

user_table_create = ("""
 CREATE TABLE users (
        user_id int,
        first_name varchar,
        last_name varchar,
        gender varchar,
        level varchar
    );
""")

song_table_create = ("""
 CREATE TABLE songs (
        song_id varchar,
        title varchar,
        artist_id varchar,
        year int,
        duration numeric
    );
""")

artist_table_create = ("""
 CREATE TABLE artists (
        artist_id varchar,
        artist_name varchar,
        artist_location varchar,
        artist_latitude numeric,
        artist_longitude numeric
    );
""")

time_table_create = ("""
 CREATE TABLE time (
        start_time timestamp,
        hour int,
        day int,
        week int,
        month int,
        year int,
        weekday int
    );
""")

# INSERT RECORDS

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = (f"""
    INSERT INTO songs
    VALUES
    (%s, %s, %s, %s, %s)
""")

artist_table_insert = ("""
    INSERT INTO artists
    VALUES
    (%s, %s, %s, %s, %s)

""")


time_table_insert = ("""
    INSERT INTO time
    VALUES
    (%s, %s, %s, %s, %s, %s, %s)
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]