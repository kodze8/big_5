import json
from collections import Counter
import pandas as pd
from model import genre_mapper, spotify_listening_info


def __mapped_listened_genres(playlistID):
    listened_genres = spotify_listening_info.genre_listened(playlistID)
    if listened_genres is None:
        return None

    with open("/Users/saikodze/PycharmProjects/WhatYouListen_WhoYouAre/model/genre_dict.json", "r") as file:
        mapper = json.load(file)

    mapped_genres = []
    for x in listened_genres:
        try:
            mapped_genres.append(mapper[x])
        except KeyError:
            # already mapped most popular spotify genres into data genres
            # but if there is something unseen in listening playlist
            # I tried to map it also to data genre
            for word in genre_mapper.DATA_GENRES:
                spotify_genre = "".join("".join(x.split(" ")).split("-")).lower()
                data_genre = "".join("".join(word.split(" ")).split("-")).lower()
                if spotify_genre in data_genre or data_genre in spotify_genre:
                    mapped_genres.append(word)
                    break
    return dict(Counter(mapped_genres))


def big_5_scores(playlist_id):
    mapped_genres = __mapped_listened_genres(playlist_id)
    if mapped_genres is None:
        return None

    with open("/Users/saikodze/PycharmProjects/WhatYouListen_WhoYouAre/model/correlation.csv", "r") as file:
        df = pd.read_csv(file)

    df.set_index("Genres", inplace=True, drop=True)
    df.dropna(inplace=True)

    total = sum([v for k, v in mapped_genres.items()])

    indexes_to_drop = [x for x in df.index if x not in mapped_genres.keys()]
    df = df.drop(indexes_to_drop)

    # multiply correlation coefficients to number of times genre was listened
    for genre, weight in mapped_genres.items():
        df.loc[genre] = df.loc[genre].apply(lambda x: weight * x)

    # exaggerate scores
    big_5 = {}
    for trait in df.columns:
        big_5[trait] = 5 + round((((df[trait].sum() / total) * 10) * 10) / 2)
    return big_5


def persinality_description(scores):
    with open("/Users/saikodze/PycharmProjects/WhatYouListen_WhoYouAre/model/Chat_GPT_personality_spectrum.json", "r") as file:
        spectrum = json.load(file)
    summery =""
    for k, v in scores.items():
        if -1 < v < 11:
            summery += spectrum[k][str(v)]
    return summery




