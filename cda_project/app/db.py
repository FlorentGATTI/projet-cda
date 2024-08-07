import logging
from pymongo import MongoClient

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
            self.client = MongoClient("mongodb://localhost:27017")
            logging.info(f"MongoClient initialized: {self.client}")
            self.db = self.client["cda"]
            collections = self.db.list_collection_names()
            logging.info(f"Connected to 'cda' database. Collections: {collections}")
        except Exception as e:
            logging.error(f"Failed to start MongoDB client: {e}")
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
