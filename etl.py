import os
import glob
import psycopg2
import time

import create_tables
from sql_queries import *


def stage_song_data(cur, filepath):
    """Loads json song data into staging table"""
    cur.execute(load_song_data_stage % filepath)


def load_song_data(cur):
    """Loads data from staging table into songs and artists tables"""
    cur.execute(songs_load)
    cur.execute(artists_load)


def stage_log_data(cur, filepath):
    """Loads json log data into staging table"""
    cur.execute(load_log_data_stage % filepath)


def load_log_data(cur):
    """Loads json log data into staging table"""
    cur.execute(filter_log_data_stage)
    cur.execute(time_load)
    cur.execute(users_load)
    cur.execute(songplays_load)


def process_data(cur, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print(f'{num_files} files found in {filepath}')

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        print(f'{i}/{num_files} files processed.')


def main():
    create_tables.main()
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    process_data(cur, filepath='data/song_data', func=stage_song_data)
    load_song_data(cur)

    process_data(cur, filepath='data/log_data', func=stage_log_data)
    load_log_data(cur)

    conn.close()


if __name__ == "__main__":
    st = time.time()
    main()
    print(f'runtime: {time.time() - st}')
