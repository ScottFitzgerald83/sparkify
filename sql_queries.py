# DROP TABLES LIST
tables = ['song_data_stage', 'log_data_stage', 'songplay', 'users', 'songs', 'artists', 'time']

# STAGING TABLES
song_data_stage_create = "CREATE TABLE song_data_stage (data jsonb);"
log_data_stage_create = "CREATE TABLE log_data_stage (data jsonb);"

# DATA (PRODUCTION) TABLES CREATE STATEMENTS
songs_create = ("""
    CREATE TABLE songs (
        song_id VARCHAR PRIMARY KEY,
        title VARCHAR NOT NULL,
        artist_id VARCHAR NOT NULL,
        year INT,
        duration FLOAT
    );
""")

artists_create = ("""
    CREATE TABLE artists (
        artist_id VARCHAR PRIMARY KEY,
        artist_name VARCHAR NOT NULL,
        artist_location VARCHAR,
        artist_latitude FLOAT,
        artist_longitude FLOAT
    );
""")

time_create = ("""
    CREATE TABLE time (
        start_time timestamp PRIMARY KEY,
        hour INT,
        day INT,
        week INT,
        month INT,
        year INT,
        weekday INT
    );
""")

users_create = ("""
    CREATE TABLE users (
        user_id INT PRIMARY KEY,
        first_name VARCHAR,
        last_name VARCHAR,
        gender VARCHAR,
        level VARCHAR
    );
""")

songplays_create = ("""
    CREATE TABLE songplays (
        songplay_id serial PRIMARY KEY,
        start_time timestamp NOT NULL,
        user_id INT NOT NULL,
        level VARCHAR,
        song_id VARCHAR,
        artist_id VARCHAR,
        session_id INT NOT NULL,
        location VARCHAR,
        user_agent VARCHAR
    );
""")

# INSERT RECORDS

# Load song data from json file into staging table
load_song_data_stage = "COPY song_data_stage FROM '%s';"

# Load log data from json into staging table and filter by page = NextSong
# postgres doesn't like escaped quotes in json: https://stackoverflow.com/questions/44997087/
load_log_data_stage = "COPY log_data_stage FROM '%s' WITH (FORMAT CSV, QUOTE '|', DELIMITER E'\t');"
filter_log_data_stage = "DELETE FROM log_data_stage WHERE data ->> 'page' != 'NextSong'"

# Load song data from staging table into songs
songs_load = """
    INSERT INTO songs    
    SELECT
        data ->> 'song_id' AS song_id,
        data ->> 'title' AS title,
        data ->> 'artist_id' AS artist_id,
        (data ->> 'year')::INT AS year,
        (data ->> 'duration')::FLOAT AS duration
    FROM song_data_stage;
"""

# Load artist data from staging table into artists
artists_load = """
    INSERT INTO artists
    SELECT DISTINCT 
        data ->> 'artist_id' AS artist_id,
        data ->> 'artist_name' AS artist_name,
        data ->> 'artist_location' AS artist_location,
        (data ->> 'artist_latitude')::FLOAT AS artist_latitude,
        (data ->> 'artist_longitude')::FLOAT AS artist_longitude
    FROM song_data_stage;
"""

# Load unique users from staging table into users
# For users with multiple levels, selects the latest level
users_load = """
    INSERT INTO users
    SELECT
        DISTINCT ON (user_id) user_id,
        first_name,
        last_name,
        gender,
        level
    FROM (
        SELECT
            data ->> 'ts' AS ts,
            (data ->> 'userId')::INT AS user_id,
            data ->> 'firstName' AS first_name,
            data ->> 'lastName' AS last_name,
            data ->> 'gender' AS gender,
            data ->> 'level' AS level
        FROM log_data_stage
        ORDER BY ts DESC
    ) users_temp
    ON CONFLICT (user_id) DO UPDATE SET level = EXCLUDED.level
"""

# Extract, convert, and split log timestamps to load into time table
time_load = """
    INSERT into TIME
    SELECT DISTINCT
      ts,
      extract(hour FROM ts)::INT AS hour,
      extract(day FROM ts)::INT AS day,
      extract(week FROM ts)::INT AS week,
      extract(month FROM ts)::INT AS month,
      extract(year FROM ts)::INT AS year,
      extract(isodow FROM ts)::INT AS weekday
    FROM (
      SELECT 
        (to_timestamp((data ->> 'ts')::bigint/ 1000))::timestamp ts 
      FROM log_data_stage
    ) next_song_ts
"""

# Load songplays data from staging table, joining on songs and artists
songplays_load = """
    INSERT INTO songplays (start_time, user_id, LEVEL, song_id, artist_id, session_id, LOCATION, user_agent)
    SELECT
      to_timestamp((data ->> 'ts')::bigint/ 1000)::timestamp,
      (data ->> 'userId')::INT,
      data ->> 'level' AS level,
      s.song_id,
      a.artist_id,
      (data ->> 'sessionId')::INT AS session_id,
      data ->> 'location' AS song,
      data ->> 'userAgent' AS artist
    FROM log_data_stage
    LEFT JOIN songs s ON s.title = data ->> 'song'
    LEFT JOIN artists a ON artist_name = data ->> 'artist'
"""
# QUERY AND TABLE LISTS

create_table_queries = [song_data_stage_create, log_data_stage_create, songs_create, artists_create, time_create,
                        users_create, songplays_create]
