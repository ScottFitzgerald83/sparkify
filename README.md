
# [WIP] Sparkify
This is project 1 of the [Udacity Data Engineer nanodegree](https://www.udacity.com/course/data-engineer-nanodegree--nd027). The goal is to create a Postgres database designed to optimize queries on song play analysis. The first dataset is a subset of real data from the [Million Song Dataset](https://labrosa.ee.columbia.edu/millionsong/) and the second dataset is JSON logs generated by [this event simulator](https://github.com/Interana/eventsim).

From the project description:
>A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

That said, the main project goal are to provide the analytics team a way to easily query the songs that users are listening to. This README seeks to convey:
1. The purpose of the database
2. Schema explanation and rationale, plus ETL explanation
3. Requirements
4. Getting started with the data
5. Sample queries

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
Below are an explanation of the database and a walkthrough of how the ETL works.

### Schema design
This section explains the table structures and how they relate to one another. Below is a list of each table along with the following:
1. Table name and description
2. Columns and data types for each table
3. Column constraints, if any
4. An explanation of the data in each column
5. An example query from each table

#### Songs table
Table name: `songs`
Description: A collection of unique songs found across all the `song_data` JSON logs.
##### Table structure
|Column|Type|Modifiers|Description|
|-|-|-|-|
| `song_id`   | character varying |  not null primary key  |A string value identifying the unique song, e.g. `SONHOTT12A8C13493C`|
| `title`     | character varying |  not null   |The song's title, e.g. `Something Girls`|
| `artist_id` | character varying |  not null   |A string value identifying the artist, e.g. `AR7G5I41187FB4CE6C`|
| `year`      | integer           |             |The year the song was released, e.g. `1982`|
| `duration`  | double precision  |             |Song length in seconds, e.g. `233.40363`|
##### Example
| song_id            | title           | artist_id          | year   | duration   |
|-|-|-|-|-|
| SONHOTT12A8C13493C | Something Girls | AR7G5I41187FB4CE6C | 1982   | 233.40363  |
| SOIAZJW12AB01853F1 | Pink World      | AR8ZCNI1187B9A069B | 1984   | 269.81832  |
| SOFSOCN12A8C143F5D | Face the Ashes  | ARXR32B1187FB57099 | 2007   | 209.60608  |

#### Artists table
Table name: `artists`
Description: A collection of each unique artist found across the `song_data` JSON, including their location, if available.

##### Table structure
| Column           | Type              | Modifiers   | Description |
|-|-|-|-|
| `artist_id`        | character varying |  not null  primary key |A string value identifying the artist, e.g. `AR9AWNF1187B9AB0B4`
| `artist_name`     | character varying |  not null   | The artist's name, e.g. `Kenny G featuring Daryl Hall`
| `artist_location`  | character varying |             |Artist's city and state, `Seattle, Washington USA`
| `artist_latitude`  | double precision  |             |Artist's latitude, if provided, e.g., `32.74863`
| `artist_longitude` | double precision  |             |Artist's longitude, if provided, e.g., `-97.32925`

##### Example
| artist_id          | artist_name                  | artist_location         | artist_latitude   | artist_longitude   |
|-|-|-|-|-|
| ARLTWXK1187FB5A3F8 | King Curtis     | Fort Worth, TX    | 32.74863          | -97.32925          |
| AR3JMC51187B9AE49D | Backstreet Boys | Orlando, FL       | 28.53823          | -81.37739          |
| ARAJPHH1187FB5566A | The Shangri-Las | Queens, NY        | 40.7038           | -73.83168          |
#### Users table
Table name: `users`
Description: Data about each user found in the songplay `log_data` JSON, including gender and pricing tier.

##### Table structure
| Column     | Type              | Modifiers   | Description|
|-|-|-|-
| `user_id`    | integer           |  not null primary key  |The id associated with the user 
| `first_name` | character varying |             |User's first name
| `last_name`  | character varying |             |User's last name
| `gender`     | character varying |             |User-provided gender 
| `level`      | character varying |             |The user's pricing tier

##### Example
| user_id   | first_name   | last_name   | gender   | level   |
|-|-|-|-|-|
| 2         | Jizelle      | Benjamin    | F        | free    |
| 3         | Isaac        | Valdez      | M        | free    |
| 4         | Alivia       | Terrell     | F        | free    |

#### Time table
Table name: `time`
Description: timestamps of user songplays broken down into numeric values of the various date part units from that timestamp

##### Table structure
| Column     | Type                        | Modifiers   | Description
|-|-|-|-|
| `start_time` | timestamp without time zone |  not null   | The start time of a songplay
| `hour`       | integer                     |             | Numeric value of hour 
| `day`        | integer                     |             | Numeric value of day 
| `week`       | integer                     |             | Numeric value of week 
| `month`      | integer                     |             | Numeric value of month
| `year`       | integer                     |             | Numeric value of year
| `weekday`    | integer                     |             | Numeric value of weekday
##### Example
| start_time          | hour   | day   | week   | month   | year   | weekday   |
|-|-|-|-|-|-|-|
| 2018-11-15 18:04:48 | 18     | 15    | 46     | 11      | 2018   | 4         |
| 2018-11-16 04:06:55 | 4      | 16    | 46     | 11      | 2018   | 5         |

#### Songplays table
Table name: `songplays`
Description: Song and user data for each individual songplay

##### Table structure
|Column|Type|Modifiers|description|
|-|-|-|-|
| songplay_id | serial                     |  not null default  | An incrementing index to track songplays
| start_time  | timestamp without time zone |  not null                                                        | The datetime the songplay started
| user_id     | integer                     |  not null                                                        | The ID of the user who initiated the songplay
| level       | character varying           |                                                                  | The user's pricing tier
| song_id     | character varying           |                                                                  | The ID of the song being listened to 
| artist_id   | character varying           |                                                                  | The ID of the artist being listened to 
| session_id  | integer                     |  not null                                                        | The user's session ID
| location    | character varying           |                                                                  | The user's location during songplay
| user_agent  | character varying           |                                                                  | The user agent that triggered the songplay

##### Example

| songplay_id   | start_time          | user_id   | level   | song_id   | artist_id   | session_id   | location                            | user_agent                                                                                                                                  |
|-|-|-|-|-|-|-|-|-|
| 1             | 2018-11-16 05:23:00 | 80        | paid    | <null>    | <null>      | 620          | Portland-South Portland, ME         | "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"                  |
| 2             | 2018-11-22 09:04:03 | 23        | free    | <null>    | <null>      | 351          | Raleigh, NC                         | "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53" |
| 3             | 2018-11-29 16:27:31 | 80        | paid    | <null>    | <null>      | 1065         | Portland-South Portland, ME         | "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"                  |

### ETL walkthrough
* There are two types of data files stored in the `/data/` directory, both in multi-line JSON format:
	* `song_data`, which consists of song and artist data
	* `log_data`, which consists of user and songplay data
* `create_tables.py` creates the `sparkifydb`, the data tables from the above section, and two staging tables used for ETL: `song_data_stage` and `log_data_stage`. Each table has a single column with a data type of `jsonb`
* The `etl.py` script executes a series of SQL statements that can be found in `sql_queries.py` that:
	* parse the JSON in these columns 
	* perform transformations or filtering as necessary
	* load the desired JSON values into the proper target tables

## Requirements
This project was written in Python3 using `psycopg2` and Postgres 11. The python requirements are listed in `requirements.txt`. It's best to install these packages in a virtual environment (see below links):

* Python3 
* A Python virtual environment. See [Python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#targetText=To%20create%20a%20virtual%20environment,project's%20directory%20and%20run%20virtualenv.&targetText=The%20second%20argument%20is%20the,installation%20in%20the%20env%20folder.) for details.
* Postgres installation will vary by OS, see http://postgresguide.com/setup/install.html
* [Optional] [`pgcli`](https://www.pgcli.com) to interact with Postgres locally


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
There is a sample notebook in this project located at `/notebooks/sample_queries.ipynb`. Inside this notebook are the following queries.

### Top users
The ten users who listened to the most songs in this dataset
#### Query logic
```
select user_id, count(*) num_songplays
from songplays 
group by 1 order by 2 desc 
limit 10;
```
#### Results
```
+-----------+-----------------+
| user_id   | num_songplays   |
|-----------+-----------------|
| 49        | 689             |
| 80        | 665             |
| 97        | 557             |
| 15        | 463             |
| 44        | 397             |
| 29        | 346             |
| 24        | 321             |
| 73        | 289             |
| 88        | 270             |
| 36        | 248             |
+-----------+-----------------+
```
### Top  locations
The cities that listened to the most songs
```
select location as location, count(*) num_songplays
from songplays 
group by 1 order by 2 desc 
limit 10;
```
```
+-----------------------------------------+-----------------+
| location                                    | num_songplays   |
|-----------------------------------------+-----------------|
| San Francisco-Oakland-Hayward, CA       | 691             |
| Portland-South Portland, ME             | 665             |
| Lansing-East Lansing, MI                | 557             |
| Chicago-Naperville-Elgin, IL-IN-WI      | 475             |
| Atlanta-Sandy Springs-Roswell, GA       | 456             |
| Waterloo-Cedar Falls, IA                | 397             |
| Lake Havasu City-Kingman, AZ            | 321             |
| Tampa-St. Petersburg-Clearwater, FL     | 307             |
| San Jose-Sunnyvale-Santa Clara, CA      | 292             |
| Sacramento--Roseville--Arden-Arcade, CA | 270             |
+-----------------------------------------+-----------------+
```

### Top user agents
The most popular user agents used for streaming songs, by count of songs played. Survey says our users really like Firefox :)
#### Query logic
```
select user_agent, count(*) num_songplays
from songplays 
group by 1 order by 2 desc 
limit 10;
```
#### Results
```
+-------------------------------------------------------------------------------------------------------------------------------------------+-----------------+
| user_agent                                                                                                                                | num_songplays   |
|-------------------------------------------------------------------------------------------------------------------------------------------+-----------------|
| "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"                | 971             |
| "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2"                   | 708             |
| Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0                                                                         | 696             |
| "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/36.0.1985.125 Chrome/36.0.1985.125 Safari/537.36" | 577             |
| "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36"                                | 573             |
| Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:31.0) Gecko/20100101 Firefox/31.0                                                         | 443             |
| "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"                           | 427             |
| "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"                           | 419             |
| "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.77.4 (KHTML, like Gecko) Version/7.0.5 Safari/537.77.4"                   | 319             |
| Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0                                                                  | 310             |
+-------------------------------------------------------------------------------------------------------------------------------------------+-----------------+
```

