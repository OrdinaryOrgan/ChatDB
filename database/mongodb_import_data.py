import os
import json
import time
import pandas as pd
from pymongo import MongoClient
from db_config import MONGODB_CONFIG, MONGODB_DATABASE

start_time = time.perf_counter()

games = pd.read_csv(r"../datasets/steam/games.csv")
games_clean = games.drop_duplicates(subset = 'gameid', keep = "first")

players = pd.read_csv(r"../datasets/steam/players.csv")
players_clean = players.drop_duplicates(subset = 'playerid', keep = "first")

reviews = pd.read_csv(r"../datasets/steam/reviews.csv")
reviews_clean = reviews.drop_duplicates(keep = "first")

valid_gameid_set = set(games_clean["gameid"].unique())
valid_playerid_set = set(players_clean["playerid"].unique())

reviews_clean = reviews_clean[reviews_clean["gameid"].isin(valid_gameid_set) & reviews_clean["playerid"].isin(valid_playerid_set)]

games_clean.to_json(r"../datasets/steam/games.json", orient = 'records', indent = 4)
players_clean.to_json(r"../datasets/steam/players.json", orient = 'records', indent = 4)
reviews_clean.to_json(r"../datasets/steam/reviews.json", orient = 'records', indent = 4)

end_time1 = time.perf_counter()
print(f'Data cleaning takes: {end_time1 - start_time:.4f} seconds')

client = MongoClient(**MONGODB_CONFIG)
db = client[MONGODB_DATABASE]

file_path = r'../datasets/steam/'
collections = ['games', 'players', 'reviews']
for collection in collections:
    data_path = os.path.join(file_path, collection + '.json')
    with open(data_path, "r", encoding = "utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                db[collection].insert_many(data)
            elif isinstance(data, dict):
                db[collection].insert_one(data)
            print(f'{collection} data inserted')
        except Exception as e:
            print(f'{collection} error: {e}')
print(f'Data insertion takes: {time.perf_counter() - end_time1:.4f} seconds')