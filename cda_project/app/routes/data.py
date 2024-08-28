from fastapi import APIRouter, HTTPException
from app.models.data import TotalBirths
from app.db import mongodb_client
import logging

router = APIRouter()

@router.get("/total_births/{year}", response_model=TotalBirths)
def get_total_births(year: int):
    logging.info("Received request for total births")
    logging.info(f"Current state of mongodb in route: {mongodb_client.db}")
    if not mongodb_client.db:
        logging.error("Database connection not established")
        raise HTTPException(status_code=500, detail="Database connection not established")
    
    logging.info(f"Fetching total births for year: {year}")
    births_by_year = list(mongodb_client.db["prenoms"].aggregate([
        {"$match": {"Year": year}},
        {"$group": {"_id": "$Year", "total_births": {"$sum": "$Count"}}}
    ]))
    if not births_by_year:
        logging.warning(f"No data found for year: {year}")
        raise HTTPException(status_code=404, detail="Year not found")
    logging.info(f"Total births for year {year}: {births_by_year[0]['total_births']}")
    return {"year": year, "total_births": births_by_year[0]["total_births"]}

@router.get("/births_by_sex/{year}")
def get_births_by_sex(year: int):
    try:
        if not mongodb_client.db:
            logging.error("Database connection not established")
            raise HTTPException(status_code=500, detail="Database connection not established")
        
        births_by_sex = list(mongodb_client.db["prenoms"].aggregate([
            {"$match": {"Year": year}},
            {"$group": {"_id": "$Sex", "total_births": {"$sum": "$Count"}}}
        ]))
        result = {item["_id"]: item["total_births"] for item in births_by_sex}
        
        if not result:
            raise HTTPException(status_code=404, detail=f"No data found for year {year}")
        
        return result
    except Exception as e:
        logging.error(f"Error fetching births by sex for year {year}: {e}")
        raise HTTPException(status_code=500, detail=str(e))