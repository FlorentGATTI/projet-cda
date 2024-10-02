from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from scripts.analysis import (
    study_trends,
    measure_diversity,
    analyze_name_length,
    analyze_by_decade,
)
from app.db import get_cached_data, get_cached_pivot_table
import logging
import plotly.utils

router = APIRouter()

def plot_to_json(fig):
    return plotly.utils.PlotlyJSONEncoder().encode(fig)

@router.get("/plots/diversity")
def get_diversity_plot():
    try:
        pivot_table = get_cached_pivot_table()
        fig = measure_diversity(pivot_table)
        if fig is None:
            raise HTTPException(status_code=404, detail="No data available for diversity plot")
        return JSONResponse(content={"figure": plot_to_json(fig)})
    except Exception as e:
        logging.error(f"Error in get_diversity_plot: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while generating the diversity plot")

@router.get("/plots/name_length")
def get_name_length_plot():
    try:
        data = get_cached_data()
        fig = analyze_name_length(data)
        if fig is None:
            raise HTTPException(status_code=404, detail="No data available for name length plot")
        return JSONResponse(content={"figure": plot_to_json(fig)})
    except Exception as e:
        logging.error(f"Error in get_name_length_plot: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while generating the name length plot")

@router.get("/plots/decade_analysis")
def get_decade_analysis_plot():
    try:
        data = get_cached_data()
        fig = analyze_by_decade(data)
        if fig is None:
            raise HTTPException(status_code=404, detail="No data available for decade analysis plot")
        return JSONResponse(content={"figure": plot_to_json(fig)})
    except Exception as e:
        logging.error(f"Error in get_decade_analysis_plot: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while generating the decade analysis plot")

@router.get("/plots/trends")
def get_trends_plot(names: str = Query(..., description="Comma-separated list of names")):
    try:
        pivot_table = get_cached_pivot_table()
        name_list = [name.strip() for name in names.split(',') if name.strip()]
        if len(name_list) == 0:
            raise HTTPException(status_code=400, detail="At least one name must be provided")
        fig = study_trends(pivot_table, *name_list[:2])
        if fig is None:
            raise HTTPException(status_code=404, detail="No data available for the specified names")
        return JSONResponse(content={"figure": plot_to_json(fig)})
    except Exception as e:
        logging.error(f"Error in get_trends_plot: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while generating the trends plot")