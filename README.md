
# [WIP] Sparkify
This is project 1 of the [Udacity Data Engineer nanodegree](https://www.udacity.com/course/data-engineer-nanodegree--nd027). The goal is to create a Postgres database designed to optimize queries on song play analysis. The first dataset is a subset of real data from the [Million Song Dataset](https://labrosa.ee.columbia.edu/millionsong/) and the second dataset is JSON logs generated by [this event simulator](https://github.com/Interana/eventsim).

From the project description:
>A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

That said, the main project goal are to provide the analytics team a way to easily query the songs that users are listening to.

## Purpose of the database

The purpose of this database is to create a logical structure for Sparkify to store transformed logs containing song and user data. These tables provide a structure that enable Sparkify's analysts to query this data.

The `sparkify` database consists of the following tables:
|Table name|Purpose|
|-|-|
|songs|Details about each song found in the song data|
|artists|Details about each song found in the song data|
|users|Details about each song found in the log data|
|time|A collection of date parts from each songplay start time|
|songplays|Details about each song played, including both song, artist, and user data|
|song_data_stage|Staging table used during ETL to read in song data from JSON|
|log_data_stage|Staging table used during ETL to read in log data from JSON|
## Schema explanation and rationale
[TODO] State and justify your database schema design and ETL pipeline.
This section explains the table structures and keys.
### Songs table
A collection of unique songs found in the `song_data` JSON. 
Name: `songs`
|column|type|constraints|description|
|-|-|-|-|
| `song_id`   | character varying |  not null primary key  |A string value identifying the unique song, e.g. `SONHOTT12A8C13493C`|
| `title`     | character varying |  not null   |The song's title, e.g. `Something Girls`|
| `artist_id` | character varying |  not null   |A string value identifying the artist, e.g. `AR7G5I41187FB4CE6C`|
| `year`      | integer           |             |The year the song was released, e.g. `1982`|
| `duration`  | double precision  |             |Song length in seconds, e.g. `233.40363`|


### Artists table
### users table
### time table
### songplays table


## Requirements
* Python3 
* A Python virtual environment. See [Python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#targetText=To%20create%20a%20virtual%20environment,project's%20directory%20and%20run%20virtualenv.&targetText=The%20second%20argument%20is%20the,installation%20in%20the%20env%20folder.) for details.
* Postgres installation will vary by OS, see http://postgresguide.com/setup/install.html
* [Optional] [`pgcli`](https://www.pgcli.com) to interact with Postgres locally

The python requirements are listed in `requirements.txt`. It's best to install these packages in a virtual environment (see below)

## Getting started
This section will walk you through setting up your environment, the database, and running the ETL pipeline to create and populate the tables. To explore the data, see the Sample Queries section at the bottom.
### Environment setup
1. Clone this repository: `git clone git@github.com:ScottFitzgerald83/sparkify.git`
2. Navigate to the project directory: `cd sparkify`
3. Create and activate a virtual environment (venv): `python3 -m venv venv; . venv/bin/activate`
4. Use pip to install the requirements in your venv: `pip3 install -r requirements.txt`
5. Follow the Postgres steps below

### Postgres setup
This project assumes there is a database named `studentdb` and a [Postgres role](https://www.postgresql.org/docs/current/sql-createrole.html) named `student`. Furthermore the `student` role must have the following Postgres permissions in order to create the `sparkifydb` and read the data from the json files:
* `CREATEDB`
* `pg_read_server_files`

Once Postgres is installed, you'll need to connect to it issue these commands. This can be done with either `psql` or `pgcli`
1. Ensure Postgres is running
2. Connect to the default database (`postgres`): `pgcli postgres://localhost:5432/postgres`
3. Create the `studentdb` database: `CREATE DATABASE studentdb`
4. Create the `student` role with login and createdb permissions: `CREATE ROLE student WITH LOGIN CREATEDB` 
5. Grant the file read permissions: `GRANT pg_read_server_files TO STUDENT`

### Running the ETL
1. Run create_tables to create the `sparkifydb` database and tables: `python3 create_tables.py`
2. Run the ETL pipeline to load the tables: `python3 etl.py`

## Example queries
[TODO] [Optional] Provide example queries and results for song play analysis.


