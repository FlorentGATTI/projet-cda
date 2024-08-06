from pymongo import MongoClient
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient("mongodb://localhost:27017")
    app.mongodb = app.mongodb_client["cda"]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()