from fastapi import APIRouter, HTTPException
from app.models.data import TotalBirths
from scripts.load_data import load_data

data = load_data()

router = APIRouter()

@router.get("/total_births/{year}", response_model=TotalBirths)
def get_total_births(year: int):
    print(f"Requested year: {year}")
    births_by_year = data[data['Year'] == year].groupby('Year')['Count'].sum()
    if births_by_year.empty:
        raise HTTPException(status_code=404, detail="Year not found")
    return {"year": year, "total_births": births_by_year.iloc[0]}
