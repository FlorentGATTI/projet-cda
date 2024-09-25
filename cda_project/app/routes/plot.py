from fastapi import APIRouter, HTTPException
import plotly.graph_objects as go
from scripts.analysis import study_trends, measure_diversity, analyze_name_length, analyze_by_decade
from app.db import get_cached_data, get_cached_pivot_table
import logging
import base64

router = APIRouter()

@router.get("/plots/trends")
async def get_trends(name1: str = None, name2: str = None):
    try:
        data = get_cached_data()
        if data is None:
            raise HTTPException(status_code=500, detail="Database connection not established")

        pivot_table = get_cached_pivot_table()
        names = [name for name in [name1, name2] if name]

        fig = study_trends(pivot_table, names)
        if fig is None:
            raise HTTPException(status_code=400, detail="Insufficient data to generate trends plot.")

        return {"figure": fig.to_json()}
    except Exception as e:
        logging.error(f"Error generating trends plot: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/plots/name_length")
async def get_name_length():
    try:
        data = get_cached_data()
        if data is None:
            raise HTTPException(status_code=500, detail="Database connection not established")

        fig = analyze_name_length(data)
        if fig is None:
            raise HTTPException(status_code=400, detail="Insufficient data to generate name length plot.")

        return {"figure": fig.to_json()}
    except Exception as e:
        logging.error(f"Error generating name length plot: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/plots/decade_analysis")
async def get_decade_analysis():
    try:
        data = get_cached_data()
        if data is None:
            raise HTTPException(status_code=500, detail="Database connection not established")

        fig = analyze_by_decade(data)
        if fig is None:
            raise HTTPException(status_code=400, detail="Insufficient data to generate decade analysis plot.")

        return {"figure": fig.to_json()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/plots/yearly_births")
async def get_yearly_births():
    try:
        data = get_cached_data()
        if data is None:
            raise HTTPException(status_code=500, detail="Database connection not established")

        yearly_births = data.groupby('Year')['Count'].sum()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=yearly_births.index, y=yearly_births.values, mode='lines', name='Nombre de naissances'))
        fig.update_layout(title='Nombre de naissances par année', xaxis_title='Année', yaxis_title='Nombre de naissances')

        image_base64 = fig.to_image(format="png")
        return {"image": base64.b64encode(image_base64).decode('utf-8')}
    except Exception as e:
        logging.error(f"Error generating yearly births plot: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/plots/diversity")
async def get_diversity():
    try:
        pivot_table = get_cached_pivot_table()
        if pivot_table is None:
            raise HTTPException(status_code=500, detail="Database connection not established")

        fig = measure_diversity(pivot_table)
        if fig is None:
            raise HTTPException(status_code=400, detail="Insufficient data to generate diversity plot.")

        return {"figure": fig.to_json()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))