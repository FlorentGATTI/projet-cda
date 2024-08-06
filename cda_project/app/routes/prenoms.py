from fastapi import APIRouter, HTTPException
from typing import List
from scripts.load_data import load_data
from app.models.prenoms import NameData

data = load_data()

router = APIRouter()

@router.get("/top_names/{year}", response_model=List[NameData])
def get_top_names(year: int):
    top_names_by_year = data[data['Year'] == year].nlargest(1000, 'Count')
    if top_names_by_year.empty:
        raise HTTPException(status_code=404, detail="Year not found")

    filtered_names = top_names_by_year.dropna(subset=['Name', 'Count'])
    if filtered_names.empty:
        raise HTTPException(status_code=404, detail="No names found for this year")

    names_with_counts = [NameData(name=row['Name'], count=row['Count']) for index, row in filtered_names.iterrows()]
    return names_with_counts
