import pandas as pd
import json
print("Debugging: Starting script execution")
import logging
print("Debugging: Logging module imported")
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from scripts.analysis import (
    create_pivot_table,
    study_trends,
    measure_diversity,
    analyze_name_length,
    analyze_by_decade,
    analyze_geographic_diversity,
    analyze_compound_names
)
from app.db import mongodb_client, get_cached_data, get_cached_pivot_table
from functools import lru_cache

router = APIRouter()

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def plot_to_json(fig):
    return json.loads(fig.to_json())

@lru_cache(maxsize=32)
def get_cached_plot_data(names):
    data = get_cached_data()
    pivot_table = create_pivot_table(data)
    return study_trends(pivot_table, *names.split(',')[:2])

@router.get("/plots/trends")
async def get_trends(names: str = Query(..., description="Comma-separated list of names")):
    try:
        logger.info(f"Received request for trends plot with names: {names}")
        
        if mongodb_client.db is None:
            logger.error("Database connection not established")
            raise HTTPException(status_code=500, detail="Database connection not established")

        fig = get_cached_plot_data(names)
        if fig is None:
            logger.warning("Insufficient data to generate trends plot")
            raise HTTPException(status_code=404, detail="No data available for the specified names")

        logger.info("Generated plot for trends")
        return JSONResponse(content={"figure": plot_to_json(fig)})
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/plots/diversity")
def get_diversity_plot():
    try:
        pivot_table = get_cached_pivot_table()
        fig = measure_diversity(pivot_table)
        if fig is None:
            raise HTTPException(status_code=404, detail="No data available for diversity plot")
        return JSONResponse(content={"figure": plot_to_json(fig)})
    except Exception as e:
        logger.error(f"Error in get_diversity_plot: {str(e)}")
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
        logger.error(f"Error in get_name_length_plot: {str(e)}")
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
        logger.error(f"Error in get_decade_analysis_plot: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while generating the decade analysis plot")

@router.get("/plots/geographic_diversity")
def get_geographic_diversity_plot():
    try:
        data = get_cached_data()
        fig = analyze_geographic_diversity(data)
        if fig is None:
            raise HTTPException(status_code=404, detail="No data available for geographic diversity plot")
        return JSONResponse(content={"figure": plot_to_json(fig)})
    except Exception as e:
        logger.error(f"Error in get_geographic_diversity_plot: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while generating the geographic diversity plot")

@router.get("/plots/compound_names")
def get_compound_names_plot():
    try:
        data = get_cached_data()
        fig = analyze_compound_names(data)
        if fig is None:
            raise HTTPException(status_code=404, detail="No data available for compound names plot")
        json_fig = plot_to_json(fig)
        if json_fig is None:
            raise HTTPException(status_code=500, detail="Failed to convert figure to JSON")
        return JSONResponse(content={"figure": json_fig})
    except ValueError as ve:
        logger.error(f"Error in get_compound_names_plot: {str(ve)}")
        raise HTTPException(status_code=500, detail=str(ve))
    except Exception as e:
        logger.error(f"Error in get_compound_names_plot: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while generating the compound names plot")