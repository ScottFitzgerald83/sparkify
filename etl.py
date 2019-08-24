import os
import glob
import psycopg2
import pandas as pd

import create_tables
from sql_queries import *


def build_df(filepath):
    """
    Builds a dataframe from a given file. Converts json nulls to None instead of NaN
    :param filepath: the path to the file being read into the dataframe
    :return: pandas dataframe
    """
    df = pd.read_json(filepath, lines=True)
    df = df.where(pd.notnull(df), None)
    return df


def process_song_data(cur, filepath):
    """Loads json song data into staging table"""
    cur.execute(load_song_data_stage % filepath)


def load_song_data(cur, conn):
    """Loads data from staging table into songs and artists tables"""
    cur.execute(songs_load)
    cur.execute(artists_load)
    conn.commit()


def process_log_file(cur, filepath):
    # open log file
    log_df = build_df(filepath)

    # filter by NextSong action
    next_song_df = log_df.loc[log_df['page'] == 'NextSong']

    # convert timestamp column to datetime
    pd.options.mode.chained_assignment = None
    next_song_df['ts'] = pd.to_datetime(next_song_df.ts, unit='ms')
    t = next_song_df['ts']

    # insert time data records
    time_data = pd.concat([t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday], axis=1)
    column_labels = ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']

    time_df = pd.DataFrame(data=time_data.values, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = next_song_df[['userId', 'firstName', 'lastName', 'gender', 'level']].copy()

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in next_song_df.iterrows():
        # get songid and artistid from song and artist tables
        results = cur.execute(song_select, (row.song, row.artist, row.length))
        songid, artistid = results if results else None, None
        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    create_tables.main()
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_data)
    load_song_data(cur, conn)
    # process_data(cur, conn, filepath='data/song_data', func=process_song_data)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()

import time
if __name__ == "__main__":
    st = time.time()
    main()
    print(f'runtime: {time.time() - st}')
