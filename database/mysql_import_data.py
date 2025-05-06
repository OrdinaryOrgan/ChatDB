import time
import pandas as pd
from sqlalchemy import create_engine

start_time = time.perf_counter()

engine = create_engine(f"mysql+pymysql://root:root@localhost/playstation")

games = pd.read_csv(r'../datasets/playstation/games.csv')
games_clean = games.drop_duplicates(subset = 'gameid', keep = 'first')

achievements = pd.read_csv(r'../datasets/playstation/achievements.csv')
achievements_clean = achievements.drop_duplicates(subset = 'achievementid', keep = 'first')

prices = pd.read_csv(r'../datasets/playstation/prices.csv')
prices_clean = prices.drop_duplicates(subset = 'gameid', keep = 'first')

valid_game_id_set = set(games_clean['gameid'].unique())
achievements_clean = achievements_clean[achievements_clean['gameid'].isin(valid_game_id_set)]
prices_clean = prices_clean[prices_clean['gameid'].isin(valid_game_id_set)]

games_clean.to_sql(name = 'games', con = engine, if_exists = 'append', index = False, method = 'multi', chunksize = 5000)
end_time1 = time.perf_counter()
print(f"Games inserted successfully: {len(games_clean)}, takes {end_time1 - start_time:.4f} seconds.")

achievements_clean.to_sql(name = 'achievements', con = engine, if_exists = 'append', index = False, method = 'multi', chunksize = 5000)
end_time2 = time.perf_counter()
print(f"Achievements inserted successfully: {len(achievements_clean)}, takes {end_time2 - end_time1:.4f} seconds.")

prices_clean.to_sql(name = 'prices', con = engine, if_exists = 'append', index = False, method = 'multi', chunksize = 5000)
end_time3 = time.perf_counter()
print(f"Prices inserted successfully: {len(prices_clean)}, takes {end_time3 - end_time2:.4f} seconds.")