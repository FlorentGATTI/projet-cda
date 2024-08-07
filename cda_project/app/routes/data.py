from fastapi import APIRouter, HTTPException
from app.models.data import TotalBirths
from app.db import mongodb
import logging

router = APIRouter()

@router.get("/total_births/{year}", response_model=TotalBirths)
def get_total_births(year: int):
    logging.info("Received request for total births")
    if mongodb is None:
        logging.error("Database connection not established")
        raise HTTPException(status_code=500, detail="Database connection not established")
    
    logging.info(f"Fetching total births for year: {year}")
    births_by_year = list(mongodb["prenoms"].aggregate([
        {"$match": {"Year": year}},
        {"$group": {"_id": "$Year", "total_births": {"$sum": "$Count"}}}
    ]))
    if not births_by_year:
        logging.warning(f"No data found for year: {year}")
        raise HTTPException(status_code=404, detail="Year not found")
    logging.info(f"Total births for year {year}: {births_by_year[0]['total_births']}")
    return {"year": year, "total_births": births_by_year[0]["total_births"]}


# from fastapi import APIRouter, HTTPException
# from app.models.data import TotalBirths
# from scripts.load_data import load_data

# data = load_data()

# router = APIRouter()

# @router.get("/total_births/{year}", response_model=TotalBirths)
# def get_total_births(year: int):
#     print(f"Requested year: {year}")
#     births_by_year = data[data['Year'] == year].groupby('Year')['Count'].sum()
#     if births_by_year.empty:
#         raise HTTPException(status_code=404, detail="Year not found")
#     return {"year": year, "total_births": births_by_year.iloc[0]}
