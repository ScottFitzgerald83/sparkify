# CREATE TABLES
table_list = ['song_data_stage', 'log_data_stage', 'songplay',  'users',  'songs',  'artists',  'time']

# STAGING TABLES
create_song_data_stage = "CREATE TABLE song_data_stage (data jsonb);"
create_log_data_stage = "CREATE TABLE log_data_stage (data jsonb);"

songplay_table_create = ("""
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

load_song_data_stage = "COPY song_data_stage FROM '%s';"

# postgres doesn't like escaped double quotes in json
# https://stackoverflow.com/questions/44997087/insert-json-into-postgresql-that-contains-quotation-marks
load_log_data_stage = "copy log_data_stage from '%s' with (format csv, quote '|', delimiter E'\t');"

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

artists_load = """
    INSERT INTO artists
    SELECT
        data ->> 'artist_id' as artist_id,
        data ->> 'artist_name' as artist_name,
        data ->> 'artist_location' as artist_location,
        (data ->> 'artist_latitude')::numeric as artist_latitude,
        (data ->> 'artist_longitude')::numeric as artist_longitude
    FROM song_data_stage;
"""

songplay_table_insert = ("""
    INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, 
            user_agent)
    VALUES 
    (%s, %s, %s, %s, %s, %s, %s, %s)
""")

users_load = """
    INSERT INTO users
    SELECT DISTINCT
        (data ->> 'userId')::int as userId, 
        data ->> 'firstName' as firstName, 
        data ->> 'lastName' as lastName, 
        data ->> 'gender' as gender, 
        data ->> 'level' as level
    FROM log_data_stage
    WHERE data ->> 'userId' != ''
    AND data ->> 'page' = 'NextSong'
    
       
"""
user_table_insert = ("""
    INSERT INTO users
    VALUES
    (%s, %s, %s, %s, %s)

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
    SELECT s.title, a.artist_name, s.duration 
        FROM songs s 
        JOIN artists a ON a.artist_id = s.artist_id
        WHERE s.title = %s
        AND a.artist_name = %s
        AND s.duration = %s;
""")

# HELPERS

epoch_millis_to_datetime = "select to_timestamp(%s / 1000)"

# QUERY AND TABLE LISTS

create_table_queries = [
    create_song_data_stage,
    create_log_data_stage,
    songplay_table_create,
    user_table_create,
    song_table_create,
    artist_table_create,
    time_table_create
]

load_table_queries = [songs_load, artists_load]
