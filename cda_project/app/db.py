import logging
from pymongo import MongoClient

mongodb_client = None
mongodb = None

def startup_db_client():
    global mongodb_client
    global mongodb
    logging.info("Starting up MongoDB client...")
    try:
        mongodb_client = MongoClient("mongodb://localhost:27017/")
        mongodb = mongodb_client["cda"]
        # Test the connection by fetching a list of collections
        collections = mongodb.list_collection_names()
        logging.info(f"MongoDB client started and connected to 'cda' database. Collections: {collections}")
    except Exception as e:
        logging.error(f"Failed to start MongoDB client: {e}")

def shutdown_db_client():
    global mongodb_client
    global mongodb
    logging.info("Shutting down MongoDB client...")
    if mongodb_client:
        try:
            mongodb_client.close()
            mongodb_client = None
            mongodb = None
            logging.info("MongoDB client shut down.")
        except Exception as e:
            logging.error(f"Failed to shut down MongoDB client: {e}")
