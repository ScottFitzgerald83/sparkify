# DROP TABLES LIST
tables = ['song_data_stage', 'log_data_stage', 'songplay', 'users', 'songs', 'artists', 'time']

# STAGING TABLES
song_data_stage_create = "CREATE TABLE song_data_stage (data jsonb);"
log_data_stage_create = "CREATE TABLE log_data_stage (data jsonb);"

# DATA (PRODUCTION) TABLES CREATE STATEMENTS
songs_create = ("""
    CREATE TABLE songs (
        song_id varchar primary key,
        title varchar not null,
        artist_id varchar not null,
        year int,
        duration float
    );
""")

artists_create = ("""
    CREATE TABLE artists (
        artist_id varchar primary key,
        artist_name varchar not null,
        artist_location varchar,
        artist_latitude float,
        artist_longitude float
    );
""")

time_create = ("""
    CREATE TABLE time (
        start_time timestamp primary key,
        hour int,
        day int,
        week int,
        month int,
        year int,
        weekday int
    );
""")

users_create = ("""
    CREATE TABLE users (
        user_id int,
        first_name varchar,
        last_name varchar,
        gender varchar,
        level varchar
    );
""")

songplays_create = ("""
    CREATE TABLE songplays (
        songplay_id serial,
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

# INSERT RECORDS

# Load song data from json file into staging table
load_song_data_stage = "COPY song_data_stage FROM '%s';"

# Load log data from json into staging table and filter by page = NextSong
# postgres doesn't like escaped quotes in json: https://stackoverflow.com/questions/44997087/
load_log_data_stage = "copy log_data_stage from '%s' with (format csv, quote '|', delimiter E'\t');"
filter_log_data_stage = "delete from log_data_stage where data ->> 'page' != 'NextSong'"

# Load song data from staging table into songs
songs_load = """
    INSERT INTO songs    
    SELECT
        data ->> 'song_id' as song_id,
        data ->> 'title' as title,
        data ->> 'artist_id' as artist_id,
        (data ->> 'year')::int as year,
        (data ->> 'duration')::numeric as duration
    FROM song_data_stage;
"""

# Load artist data from staging table into artists
artists_load = """
    INSERT INTO artists
    SELECT DISTINCT 
        data ->> 'artist_id' as artist_id,
        data ->> 'artist_name' as artist_name,
        data ->> 'artist_location' as artist_location,
        (data ->> 'artist_latitude')::numeric as artist_latitude,
        (data ->> 'artist_longitude')::numeric as artist_longitude
    FROM song_data_stage;
"""

# Load unique users from staging table into users
users_load = """
    INSERT INTO users
    SELECT DISTINCT
        (data ->> 'userId')::int as userId, 
        data ->> 'firstName' as firstName, 
        data ->> 'lastName' as lastName, 
        data ->> 'gender' as gender, 
        data ->> 'level' as level
    FROM log_data_stage
"""

# Extract, convert, and split log timestamps to load into time table
time_load = """
    INSERT into TIME
    SELECT DISTINCT
      ts,
      extract(hour from ts)::int as hour,
      extract(day from ts)::int as day,
      extract(week from ts)::int as week,
      extract(month from ts)::int as month,
      extract(year from ts)::int as year,
      extract(isodow from ts)::int as weekday
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
      (data ->> 'userId')::int,
      data ->> 'level' AS level,
      s.song_id,
      a.artist_id,
      (data ->> 'sessionId')::int as session_id,
      data ->> 'location' AS song,
      data ->> 'userAgent' AS artist
    FROM log_data_stage
    left join songs s on s.title = data ->> 'song'
    left join artists a on artist_name = data ->> 'artist'
"""
# QUERY AND TABLE LISTS

create_table_queries = [song_data_stage_create, log_data_stage_create, songs_create, artists_create, time_create,
                        users_create, songplays_create]
