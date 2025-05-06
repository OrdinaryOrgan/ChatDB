from pymongo import MongoClient
from database import db_config

class MongoDBManager:
    def __init__(self):
        mongo_config = db_config.MONGODB_CONFIG
        self.client = MongoClient(**mongo_config)
        self.db = self.client[db_config.MONGODB_DATABASE]

    def __del__(self):
        self.client.close()

    def find_all(self, collection_name: str) -> list[dict]:
        collection = self.db[collection_name]
        return list(collection.find())

    def insert_one(self, collection_name: str, data: dict) -> str:
        collection = self.db[collection_name]
        result = collection.insert_one(data)
        return f"Inserted ID: {result.inserted_id}"

    def close(self):
        self.client.close()

mongodb_manager_instance = MongoDBManager()