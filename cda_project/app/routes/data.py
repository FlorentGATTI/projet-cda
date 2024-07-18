from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

# Simuler le chargement des données
from scripts.load_data import load_data

data = load_data()

class TotalBirths(BaseModel):
    year: int
    total_births: int

router = APIRouter()

@router.get("/total_births/{year}", response_model=TotalBirths)
def get_total_births(year: int):
    births_by_year = data[data['Year'] == year].groupby('Year')['Count'].sum()
    if births_by_year.empty:
        raise HTTPException(status_code=404, detail="Year not found")
    return {"year": year, "total_births": births_by_year.iloc[0]}
