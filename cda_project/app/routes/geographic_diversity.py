from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pymongo import MongoClient
import logging
from app.models.geographic_diversity import NameDataByState, NameDataByTerritory

router = APIRouter()

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["cda"]

def fetch_data(collection_name: str, query: dict):
    """
    Fonction générique pour exécuter une requête sur une collection MongoDB donnée.
    """
    try:
        logging.info(f"Query being executed in {collection_name}: {query}")  # Log pour suivre les requêtes exactes
        results = list(db[collection_name].find(query, {"_id": 0}).limit(100))
        if not results:
            logging.warning(f"No data found for query: {query}")
            raise HTTPException(status_code=404, detail="No data found for the given parameters.")
        return results
    except Exception as e:
        logging.error(f"Error fetching data from {collection_name}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the data.")

@router.get("/distinct_names_states", response_model=List[str])
def get_distinct_names_states():
    """
    Récupère les noms distincts pour les États.
    """
    try:
        names = db["names_by_state"].distinct("Name")
        return sorted(list(names))
    except Exception as e:
        logging.error(f"Error fetching distinct names for states: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the names for states.")

@router.get("/distinct_sexes", response_model=List[str])
def get_distinct_sexes(region_type: str, region: str, year: int):
    try:
        collection = "names_by_state" if region_type == "state" else "names_by_territory"
        region_field = "State" if region_type == "state" else "Territory"
        query = {region_field: region.upper(), "Year": year}
        sexes = db[collection].distinct("Sex", query)
        return sorted(sexes)
    except Exception as e:
        logging.error(f"Error fetching distinct sexes: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the sexes.")
    
@router.get("/distinct_names_territories", response_model=List[str])
def get_distinct_names_territories():
    """
    Récupère les noms distincts pour les Territoires.
    """
    try:
        names = db["names_by_territory"].distinct("Name")
        return sorted(list(names))
    except Exception as e:
        logging.error(f"Error fetching distinct names for territories: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the names for territories.")

@router.get("/distinct_years_states", response_model=List[int])
def get_distinct_years_states():
    """
    Récupère les années distinctes pour les États.
    """
    try:
        years = db["names_by_state"].distinct("Year")
        return sorted(list(years))
    except Exception as e:
        logging.error(f"Error fetching distinct years for states: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the years for states.")

@router.get("/distinct_years_territories", response_model=List[int])
def get_distinct_years_territories(region: str):
    try:
        years = db["names_by_territory"].distinct("Year", {"Territory": region.upper()})
        return sorted(years) if years else []
    except Exception as e:
        logging.error(f"Error fetching distinct years for territories: {e}")
        return []
    
@router.get("/distinct_states", response_model=List[str])
def get_distinct_states():
    try:
        states = db["names_by_state"].distinct("State")
        return sorted(states)
    except Exception as e:
        logging.error(f"Error fetching distinct states: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the states.")

@router.get("/distinct_territories", response_model=List[str])
def get_distinct_territories():
    try:
        territories = db["names_by_territory"].distinct("Territory")
        return sorted(territories)
    except Exception as e:
        logging.error(f"Error fetching distinct territories: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the territories.")

@router.get("/names_data", response_model=List[dict])
def get_names_data(
    region_type: str,
    region_name: Optional[str] = None, 
    year: Optional[int] = None, 
    sex: Optional[str] = None, 
    name: Optional[str] = None, 
    count: Optional[int] = None 
):
    try:
        query = {}
        collection_name = "names_by_state" if region_type == "state" else "names_by_territory"

        if region_type == "state" and region_name:
            query["State"] = region_name.upper()
        elif region_type == "territory" and region_name:
            query["Territory"] = region_name.upper()
        
        if year:
            query["Year"] = year
        if sex:
            query["Sex"] = sex
        if name:
            query["Name"] = {"$regex": f"^{name}", "$options": "i"}  # Recherche insensible à la casse commençant par le préfixe
        if count:
            query["Count"] = count 
        
        results = list(db[collection_name].find(query, {"_id": 0}).limit(100))
        return results
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the data.")