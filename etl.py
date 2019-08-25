import os
import glob
import psycopg2
import time

import create_tables
from sql_queries import *


def stage_song_data(cur, filepath):
    """
    Loads json song data into staging table
    :param cur: cursor from the psycopg2 connection object
    :param filepath: path to song data json file
    :return: None
    """
    cur.execute(load_song_data_stage % filepath)


def stage_log_data(cur, filepath):
    """
    Loads json log data into staging table
    :param cur: cursor from the psycopg2 connection object
    :param filepath: path to log data json file
    :return: None
    """
    cur.execute(load_log_data_stage % filepath)
    cur.execute(filter_log_data_stage)


def load_tables(cur):
    """
    Executes SQL queries that load data from staging into prod tables
    :param cur: cursor from the psycopg2 connection object
    :return: None
    """
    cur.execute(songs_load)
    cur.execute(artists_load)
    cur.execute(time_load)
    cur.execute(users_load)
    cur.execute(songplays_load)


def process_data(cur, filepath, func):
    """
    Lists files in a given directory then passes log and song files to their respective processing function
    :param cur: cursor from the psycopg2 connection object
    :param filepath: the directory where the source data files live
    :param func: the function which should operate on each file in the given directory
    :return: None
    """
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
    process_data(cur, filepath='data/log_data', func=stage_log_data)
    load_tables(cur)

    conn.close()


if __name__ == "__main__":
    t = time.time()
    main()
    print(time.time() - t)
