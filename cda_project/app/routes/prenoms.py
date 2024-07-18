from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

# Simuler le chargement des données
from scripts.load_data import load_data

data = load_data()

class NameData(BaseModel):
    name: str
    count: int

router = APIRouter()

@router.get("/top_names/{year}", response_model=List[NameData])
def get_top_names(year: int):
    top_names_by_year = data[data['Year'] == year].nlargest(1000, 'Count')
    if top_names_by_year.empty:
        raise HTTPException(status_code=404, detail="Year not found")
    
    # Filtrer les enregistrements sans 'name' ou 'count'
    filtered_names = top_names_by_year.dropna(subset=['Name', 'Count'])
    if filtered_names.empty:
        raise HTTPException(status_code=404, detail="No names found for this year")
    
    # Convertir en dictionnaires avec les champs requis
    names_with_counts = []
    for index, row in filtered_names.iterrows():
        name_data = NameData(name=row['Name'], count=row['Count'])
        names_with_counts.append(name_data)
    
    return names_with_counts
