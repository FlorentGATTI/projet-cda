import logging
from pymongo import MongoClient
from functools import lru_cache
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

class MongoDBClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
            cls._instance.client = None
            cls._instance.db = None
        return cls._instance

    def connect(self):
        logging.info("Starting up MongoDB client...")
        try:
            # Utiliser l'URL MongoDB à partir des variables d'environnement
            mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
            self.client = MongoClient(mongo_url)
            
            # Vérifier la connexion
            self.client.admin.command('ping')
            
            logging.info(f"MongoClient initialized: {self.client}")
            self.db = self.client["cda"]
            collections = self.db.list_collection_names()
            logging.info(f"Connected to 'cda' database. Collections: {collections}")
            # Assurez-vous d'appeler cette fonction au démarrage de votre application
        except Exception as e:
            logging.error(f"Failed to start MongoDB client: {e}")
            self.client = None
            self.db = None

    def disconnect(self):
        logging.info("Shutting down MongoDB client...")
        if self.client:
            try:
                self.client.close()
                self.client = None
                self.db = None
                logging.info("MongoDB client shut down.")
            except Exception as e:
                logging.error(f"Failed to shut down MongoDB client: {e}")

mongodb_client = MongoDBClient()

def startup_db_client():
    mongodb_client.connect()

def shutdown_db_client():
    mongodb_client.disconnect()

@lru_cache(maxsize=1)
def get_cached_data():
    if mongodb_client.db is None:
        return None
    data = pd.DataFrame(list(mongodb_client.db["prenoms"].find({}, {'_id': 0})))
    return data

@lru_cache(maxsize=1)
def get_cached_pivot_table():
    data = get_cached_data()
    if data is None:
        return None
    from scripts.analysis import create_pivot_table
    return create_pivot_table(data)
    mongodb_client.disconnect()