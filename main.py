import pandas as pd
import requests
from datetime import datetime, timedelta
import datetime
import database_config
import os


SPOTIFY_ID = os.environ.get('Spotify-ID')
TOKEN = 'BQDYjDUOd9-J2FmdErqmflMETw4RetQkPos-pHL9GDaE42CDlZ5KaCGzak8bacKiWcH6S9C2YACa6yRlBbcSnOWgrteqpcus000NaB93h_QDXt2oWGXVVJE6aSXFk3gGW0Wq3UXPuXxCZc0J-j5Jz3fD4ULGl321sRknhKtMhn6DZoBJPcHSsx16XFF8At1fdY_7CpXN'

# Validating the Data

def check_if_data_is_vaild(df: pd.DataFrame) -> bool:
    # Check if dataframe is empty
    if df.empty:
        print('No songs downloaded. Executon finished.')
        return False

    # Check Primary Key (pandas series is a One-dimensional ndarray  --> like a column)
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception('Primary Key is already existing')
    
    # Check nulls
    if df.isnull().values.any():
        raise Exception('Null values exising')

    return True


if __name__ == "__main__":

    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }

    today = datetime.datetime.now()
    today_unix = int(today.timestamp()) * 1000
    print(today_unix)
    last_week = today - datetime.timedelta(days=7)
    last_week_unix = int(last_week.timestamp()) * 1000


    r = requests.get(f"https://api.spotify.com/v1/me/player/recently-played?after={last_week_unix}", headers=headers)

    data = r.json()

    print(data)

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    # Extracting only the relevant bits of data from the json object      
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])
        
    # Prepare a dictionary in order to turn it into a pandas dataframe below       
    song_dict = {
        "song_name" : song_names,
        "artist_name": artist_names,
        "played_at" : played_at_list,
        "timestamp" : timestamps
    }

    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamp"])

    print(song_df)

    # Validation
    if check_if_data_is_vaild(song_df):
        print('Valid data, ready for loading to the database')


    # Loading the data in the database
    db = database_config.MyDatabase()

    create_table = """ CREATE TABLE IF NOT EXISTS my_played_tracks (
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at))
    """

    db.query_func(create_table)

    songs_insert_query = """INSERT INTO my_played_tracks (
        song_name, 
        artist_name, 
        played_at, 
        timestamp)  
        VALUES (%s, %s, %s, %s)
    """

    for i, row in song_df.iterrows():
        db.query_func(songs_insert_query, list(row))

    db.close()
