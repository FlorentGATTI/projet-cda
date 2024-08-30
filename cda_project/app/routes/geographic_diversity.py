from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pymongo import MongoClient
import logging

router = APIRouter()

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["cda"]

@router.get("/names_by_state", response_model=List[dict])
def get_names_by_state(state: Optional[str] = None, year: Optional[int] = None, sex: Optional[str] = None):
    try:
        query = {}
        if state:
            query["State"] = state
        if year:
            query["Year"] = year
        if sex:
            query["Sex"] = sex
        
        results = list(db["names_by_state"].find(query, {"_id": 0}).limit(100))
        if not results:
            raise HTTPException(status_code=404, detail="No data found for the given parameters.")
        
        return results
    except Exception as e:
        logging.error(f"Error fetching data by state: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the data.")

@router.get("/names_by_territory", response_model=List[dict])
def get_names_by_territory(territory: Optional[str] = None, year: Optional[int] = None, sex: Optional[str] = None):
    try:
        query = {}
        if territory:
            query["Territory"] = territory
        if year:
            query["Year"] = year
        if sex:
            query["Sex"] = sex
        
        results = list(db["names_by_territory"].find(query, {"_id": 0}).limit(100))
        if not results:
            raise HTTPException(status_code=404, detail="No data found for the given parameters.")
        
        return results
    except Exception as e:
        logging.error(f"Error fetching data by territory: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the data.")
