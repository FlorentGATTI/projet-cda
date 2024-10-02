from fastapi import APIRouter, HTTPException
from typing import List
from app.models.prenoms import NameData
from app.db import mongodb_client
from typing import List, Dict 
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
    logging.info(f"Top names for year {year}: {[name.name for name in names_with_counts]}")
    logging.info(f"Names with counts: {names_with_counts}")
    return names_with_counts

@router.get("/names", response_model=List[str])
async def get_filtered_names(query: str = ""):
    try:
        if mongodb_client.db is None:
            logging.error("Database connection not established")
            raise HTTPException(status_code=500, detail="Database connection not established")
        
        logging.info(f"Fetching names from the database with query: {query}")
        # Rechercher les prénoms correspondant à la requête, avec une limite de résultats
        all_names = mongodb_client.db["prenoms"].find({"Name": {"$regex": f"^{query}", "$options": "i"}}).limit(50)
        name_list = [name["Name"] for name in all_names]
        
        logging.info(f"Found {len(name_list)} names matching query: {query}")
        return sorted(name_list)  # Retourne les noms triés par ordre alphabétique
    except Exception as e:
        logging.error(f"Error fetching names: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Nouvelle route pour une plage d'années
@router.get("/total_births_range", response_model=List[Dict[str, int]])
def get_total_births_range(start_year: int, end_year: int):
    logging.info(f"Fetching total births between {start_year} and {end_year}")
    
    if mongodb_client.db is None:
        logging.error("Database connection not established")
        raise HTTPException(status_code=500, detail="Database connection not established")

    if start_year > end_year:
        logging.error(f"Invalid year range: {start_year} > {end_year}")
        raise HTTPException(status_code=400, detail="Invalid year range")
    
    # Requête MongoDB pour obtenir toutes les années dans la plage
    births_in_range = list(mongodb_client.db["prenoms"].aggregate([
        {"$match": {"Year": {"$gte": start_year, "$lte": end_year}}},
        {
            "$group": {
                "_id": "$Year",
                "total_births": {"$sum": "$Count"},
                "male_births": {"$sum": {"$cond": [{"$eq": ["$Sex", "M"]}, "$Count", 0]}},
                "female_births": {"$sum": {"$cond": [{"$eq": ["$Sex", "F"]}, "$Count", 0]}}
            }
        },
        {"$sort": {"_id": 1}}  # Tri par année
    ]))

    if not births_in_range:
        logging.warning(f"No data found between {start_year} and {end_year}")
        raise HTTPException(status_code=404, detail="No data found for the given range")

    # Transformer les résultats en un format plus lisible
    result = [
        {
            "year": item["_id"],
            "total_births": item["total_births"],
            "male_births": item["male_births"],
            "female_births": item["female_births"]
        }
    for item in births_in_range]

    return result
