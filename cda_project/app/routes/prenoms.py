from fastapi import APIRouter, HTTPException
from typing import List
from app.models.prenoms import NameData
from app.db import mongodb
import logging

router = APIRouter()

@router.get("/top_names/{year}", response_model=List[NameData])
def get_top_names(year: int):
    if mongodb is None:
        logging.error("Database connection not established")
        raise HTTPException(status_code=500, detail="Database connection not established")
    
    logging.info(f"Fetching top names for year: {year}")
    top_names_by_year = list(mongodb["prenoms"].find({"Year": year}).sort("Count", -1).limit(1000))
    if not top_names_by_year:
        logging.warning(f"No data found for year: {year}")
        raise HTTPException(status_code=404, detail="Year not found")

    filtered_names = [name for name in top_names_by_year if name.get('Name') and name.get('Count')]
    if not filtered_names:
        logging.warning(f"No names found for year: {year}")
        raise HTTPException(status_code=404, detail="No names found for this year")

    names_with_counts = [NameData(name=name['Name'], count=name['Count']) for name in filtered_names]
    logging.info(f"Top names for year {year}: {[name.name for name in names_with_counts]}")
    return names_with_counts
