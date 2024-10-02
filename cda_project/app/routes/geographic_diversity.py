import logging
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pymongo import MongoClient
from app.models.geographic_diversity import NameDataByState, NameDataByTerritory

router = APIRouter()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["cda"]

def fetch_data(collection_name: str, query: dict):
    try:
        logging.info(f"Query being executed in {collection_name}: {query}")
        results = list(db[collection_name].find(query, {"_id": 0}).limit(100))
        if not results:
            logging.warning(f"No data found for query: {query}")
            return []  # Retourne une liste vide au lieu de lever une exception
        return results
    except Exception as e:
        logging.error(f"Error fetching data from {collection_name}: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching the data: {str(e)}")

@router.get("/distinct_names_states", response_model=List[str])
def get_distinct_names_states():
    try:
        names = db["names_by_state"].distinct("Name")
        return sorted(names)
    except Exception as e:
        logging.error(f"Error fetching distinct names for states: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching the names for states: {str(e)}")

@router.get("/distinct_sexes", response_model=List[str])
def get_distinct_sexes(selected_type: str, state: Optional[str] = None, territory: Optional[str] = None, year: int = Query(...)):
    try:
        collection = "names_by_state" if selected_type == "state" else "names_by_territory"
        field = "State" if selected_type == "state" else "Territory"
        value = state if selected_type == "state" else territory
        if not value:
            raise HTTPException(status_code=400, detail="Either state or territory must be provided.")
        query = {field: value.upper(), "Year": year}
        sexes = db[collection].distinct("Sex", query)
        if not sexes:
            raise HTTPException(status_code=404, detail="No sex data found for the given parameters.")
        return sorted(sexes)
    except HTTPException as he:
        raise he
    except Exception as e:
        logging.error(f"Error fetching distinct sexes: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching the sexes: {str(e)}")

@router.get("/distinct_names_territories", response_model=List[str])
def get_distinct_names_territories():
    try:
        names = db["names_by_territory"].distinct("Name")
        return sorted(names)
    except Exception as e:
        logging.error(f"Error fetching distinct names for territories: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching the names for territories: {str(e)}")

@router.get("/distinct_years_states", response_model=List[int])
def get_distinct_years_states(state: str):
    try:
        years = db["names_by_state"].distinct("Year", {"State": state.upper()})
        return sorted(years)
    except Exception as e:
        logging.error(f"Error fetching distinct years for states: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching the years for states: {str(e)}")

@router.get("/distinct_years_territories", response_model=List[int])
def get_distinct_years_territories(territory: str):
    try:
        years = db["names_by_territory"].distinct("Year", {"Territory": territory.upper()})
        return sorted(years)
    except Exception as e:
        logging.error(f"Error fetching distinct years for territories: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching the years for territories: {str(e)}")

@router.get("/distinct_states", response_model=List[str])
def get_distinct_states():
    try:
        states = db["names_by_state"].distinct("State")
        return sorted(states)
    except Exception as e:
        logging.error(f"Error fetching distinct states: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching the states: {str(e)}")

@router.get("/distinct_territories", response_model=List[str])
def get_distinct_territories():
    try:
        territories = db["names_by_territory"].distinct("Territory")
        return sorted(territories)
    except Exception as e:
        logging.error(f"Error fetching distinct territories: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching the territories: {str(e)}")

@router.get("/names_data", response_model=List[dict])
def get_names_data(
    selected_type: str,
    state: Optional[str] = None,
    territory: Optional[str] = None,
    year: Optional[int] = None, 
    sex: Optional[str] = None, 
    name: Optional[str] = None
):
    try:
        query = {}
        collection_name = "names_by_state" if selected_type == "state" else "names_by_territory"

        if selected_type == "state" and state:
            query["State"] = state.upper()
        elif selected_type == "territory" and territory:
            query["Territory"] = territory.upper()
        else:
            raise HTTPException(status_code=400, detail="Invalid selected_type or missing state/territory.")
        
        if year:
            query["Year"] = year
        if sex:
            query["Sex"] = sex
        if name:
            query["Name"] = {"$regex": f"^{name}", "$options": "i"}
        
        results = fetch_data(collection_name, query)
        return results
    except HTTPException as he:
        if he.status_code == 404:
            return []  # Retourne une liste vide au lieu de lever une exception
        raise he
    except Exception as e:
        logging.error(f"Error fetching names data: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching the names data: {str(e)}")
