import base64
import requests
import os

SERVER_CLIENT_ID = "6f8295866afe4584937c2c020341a945"
SERVER_CLIENT_SECRET = "96d9a3d2c6344754bd1120e98fb69dbc"


def __get_token_access():
    global SERVER_CLIENT_SECRET, SERVER_CLIENT_ID
    search_endpoint = "https://accounts.spotify.com/api/token"
    data = {
        'grant_type': 'client_credentials'
    }
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(
            f'{SERVER_CLIENT_ID}:{SERVER_CLIENT_SECRET}'.encode('utf-8')).decode('utf-8')
    }
    response = requests.post(search_endpoint, data=data, headers=headers)
    token_data = response.json()["access_token"]
    return token_data


ACCESS_TOKEN = __get_token_access()


def __get_playlist(playlist_id):
    global ACCESS_TOKEN
    endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}"  # Corrected endpoint

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    if response.status_code != 200:
        return None
    else:
        return response.json()["tracks"]["items"]


# --------------Used json formats to get insight from playlists --------------
# with open("playlist.json", "w") as file:
#     json.dump(get_playlist("0xtjiam6rPVY7fhQUOaXTv"), file, indent=4)
#
#
# with open("playlist.json", "r") as file:
#      songs = json.load(file)["tracks"]["items"]

def __extract_artist_id(playlist):
    songs = playlist
    artists_dict = [x["track"]["artists"] for x in songs]
    artist_ids = [list(map(lambda artists: artists["id"], list_of_artists)) for list_of_artists in artists_dict]
    return artist_ids


def __artist_id_to_genre(artist_id):
    global ACCESS_TOKEN
    endpoint = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers).json()
    return response["genres"]


def genre_listened(playlist_id):
    playlist = __get_playlist(playlist_id)
    if playlist is None:
        return None
    else:
        artist_geners = [__artist_id_to_genre(x) for ids in __extract_artist_id(playlist) for x in ids]
        genre_dict = [genre for lst in artist_geners for genre in lst]
        return genre_dict

