import json

DATA_GENRES= ['Afropop', 'Alternative', 'Atmospheric', 'Black Metal', 'Blast',
               'Blues', 'Caribbean', 'Children', 'Chill', 'Christian', 'Classic Rock',
               'Classical', 'Comedy', 'Country', 'Death Metal', 'Deep House', 'Doom',
               'Easy Listening', 'Electro', 'Emo', 'Epic', 'Folk', 'Funk',
               'Funk Carioca', 'Gothic', 'Hip-hop', 'House', 'Indie', 'Jazz', 'Latin',
               'Metal', 'Metro', 'Modern Rock', 'Neuro', 'New Age', 'Old Country',
               'Other', 'Pop', 'Prog', 'Punk', 'R&B', 'Reggae', 'Reggaeton',
               'Regional Music\r(Brazil)', 'Regional Music\r(France)',
               'Regional Music\r(Germany)', 'Regional Music\r(Japan)',
               'Regional Music\r(Korea)', 'Regional Music\r(Mexico)',
               'Regional Music\r(SE Asia)', 'Rock', 'Sertanejo', 'Soul', 'Soundtrack',
               'Spoken', 'Synth', 'World Hip-hop', 'World Pop', 'World Punk',
               'Organic']

SPOTOFY_GENRES_PATH = "/Users/saikodze/PycharmProjects/WhatYouListen_WhoYouAre/model/spotify_genres"


def spotify_data_genre_mapper():
    global DATA_GENRES, SPOTOFY_GENRES_PATH
    with open(SPOTOFY_GENRES_PATH, "r") as file:
        spotify_genres = file.read()

    spotify_genres = spotify_genres.split("\n")

    mapper = {}
    for spotify in spotify_genres:
        for word in DATA_GENRES:
            spotify_modified = "".join("".join(spotify.split(" ")).split("-")).lower()
            word_modified = "".join("".join(word.split(" ")).split("-")).lower()
            if spotify_modified in word_modified or word_modified in spotify_modified:
                mapper[spotify.lower()] = word
                break

    with open("genre_dict.json", "w") as file:
        json.dump(mapper, file, indent=4)


if __name__ == '__main__':
    spotify_data_genre_mapper()
