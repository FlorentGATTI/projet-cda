from fastapi import APIRouter, HTTPException
from app.models.data import TotalBirths
from app.db import mongodb_client
import logging

router = APIRouter()

@router.get("/total_births/{year}", response_model=TotalBirths)
def get_total_births(year: int):
    logging.info(f"Fetching total births for year: {year}")
    if mongodb_client.db is None:
        logging.error("Database connection not established")
        raise HTTPException(status_code=503, detail="Database connection not established")
    
    try:
        births_by_year = list(mongodb_client.db["prenoms"].aggregate([
            {"$match": {"Year": year}},
            {"$group": {"_id": "$Year", "total_births": {"$sum": "$Count"}}}
        ]))
        if not births_by_year:
            logging.warning(f"No data found for year: {year}")
            raise HTTPException(status_code=404, detail="Year not found")
        
        births_by_sex = list(mongodb_client.db["prenoms"].aggregate([
            {"$match": {"Year": year}},
            {"$group": {"_id": "$Sex", "total_births": {"$sum": "$Count"}}}
        ]))
        result = {item["_id"]: item["total_births"] for item in births_by_sex}
        
        return {
            "year": year,
            "total_births": births_by_year[0]["total_births"],
            "births_by_sex": result or {}
        }
    except Exception as e:
        logging.error(f"Error fetching data for year {year}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/total_births/{year}", response_model=TotalBirths)
def get_total_births(year: int):
    logging.info(f"Fetching total births for year: {year}")
    if not mongodb_client.db:
        logging.error("Database connection not established")
        raise HTTPException(status_code=500, detail="Database connection not established")
    
    births_by_year = list(mongodb_client.db["prenoms"].aggregate([
        {"$match": {"Year": year}},
        {"$group": {"_id": "$Year", "total_births": {"$sum": "$Count"}}}
    ]))
    if not births_by_year:
        logging.warning(f"No data found for year: {year}")
        raise HTTPException(status_code=404, detail="Year not found")
    
    births_by_sex = list(mongodb_client.db["prenoms"].aggregate([
        {"$match": {"Year": year}},
        {"$group": {"_id": "$Sex", "total_births": {"$sum": "$Count"}}}
    ]))
    result = {item["_id"]: item["total_births"] for item in births_by_sex}
    
    return {
        "year": year,
        "total_births": births_by_year[0]["total_births"],
        "births_by_sex": result or {}  # Assurez-vous que ce champ est toujours présent
    }
