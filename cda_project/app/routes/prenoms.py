from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

# Simuler le chargement des données
from scripts.load_data import load_data

data = load_data()
top_names = data.nlargest(1000, 'Count')

class NameData(BaseModel):
    name: str
    count: int

router = APIRouter()

@router.get("/top_names/{year}", response_model=List[NameData])
def get_top_names(year: int):
    top_names_by_year = top_names[top_names['Year'] == year]
    if top_names_by_year.empty:
        raise HTTPException(status_code=404, detail="Year not found")
    return top_names_by_year[['Name', 'Count']].to_dict(orient='records')
