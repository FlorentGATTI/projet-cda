from fastapi import APIRouter, HTTPException
from typing import List
from app.models.prenoms import NameData
from app.db import mongodb_client
import logging

router = APIRouter()

@router.get("/top_names/{year}", response_model=List[NameData])
def get_top_names(year: int):
    logging.info(f"Received year: {year}")
    if mongodb_client.db is None:
        logging.error("Database connection not established")
        raise HTTPException(status_code=500, detail="Database connection not established")
    
    logging.info(f"Fetching top names for year: {year}")
    top_names_by_year = list(mongodb_client.db["prenoms"].find({"Year": year}).sort("Count", -1).limit(1000))
    
    logging.info(f"Top names fetched: {top_names_by_year}")
    if not top_names_by_year:
        logging.warning(f"No data found for year: {year}")
        raise HTTPException(status_code=404, detail="Year not found")

    filtered_names = [name for name in top_names_by_year if name.get('Name') and name.get('Count')]
    logging.info(f"Filtered names: {filtered_names}")
    
    if not filtered_names:
        logging.warning(f"No names found for year: {year}")
        raise HTTPException(status_code=404, detail="No names found for this year")

    names_with_counts = [NameData(name=name['Name'], count=name['Count']) for name in filtered_names]
    logging.info(f"Names with counts: {names_with_counts}")
    return names_with_counts

@router.get("/names", response_model=List[str])
async def get_all_names():
    try:
        if mongodb_client.db is None:
            logging.error("Database connection not established")
            raise HTTPException(status_code=500, detail="Database connection not established")
        
        logging.info("Fetching all names from the database")
        all_names = mongodb_client.db["prenoms"].distinct("Name")  # Utilisation de distinct pour obtenir tous les noms uniques
        logging.info(f"Found {len(all_names)} unique names")
        
        if not all_names:
            logging.warning("No names found in the database")
            raise HTTPException(status_code=404, detail="No names found")
        
        return sorted(all_names)  # Retourne les noms triés par ordre alphabétique
    except Exception as e:
        logging.error(f"Error fetching all names: {e}")
        raise HTTPException(status_code=500, detail=str(e))
