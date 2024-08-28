from fastapi import APIRouter, HTTPException
import pandas as pd
from scripts.analysis import create_pivot_table, study_trends, measure_diversity, analyze_name_length, analyze_by_decade, analyze_compound_names, analyze_geographic_diversity
from app.db import mongodb_client
import logging

router = APIRouter()

@router.get("/plots/trends")
async def get_trends(names: str):
    try:
        if mongodb_client.db is None:
            logging.error("Database connection not established")
            raise HTTPException(status_code=500, detail="Database connection not established")

        logging.info("Loading data from MongoDB for trends plot")
        data = pd.DataFrame(list(mongodb_client.db["prenoms"].find({})))
        logging.info(f"Loaded data with names: {names}")
        pivot_table = create_pivot_table(data)
        logging.info(f"Pivot table data: {pivot_table.head()}")
        name_list = names.split(',')
        plot_image = study_trends(pivot_table, name_list)
        if not plot_image:
            logging.warning("Insufficient data to generate trends plot")
            raise HTTPException(status_code=400, detail="Insufficient data to generate trends plot.")
        logging.info(f"Generated plot for trends: {plot_image[:100]}")
        return {"image": plot_image}
    except Exception as e:
        logging.error(f"Error generating trends plot: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/plots/diversity")
async def get_diversity():
    try:
        if mongodb_client.db is None:
            logging.error("Database connection not established")
            raise HTTPException(status_code=500, detail="Database connection not established")

        logging.info("Loading data from MongoDB for diversity plot")
        data = pd.DataFrame(list(mongodb_client.db["prenoms"].find({})))
        logging.info("Loaded data")
        pivot_table = create_pivot_table(data)
        logging.info(f"Pivot table data: {pivot_table.head()}")
        plot_image = measure_diversity(pivot_table)
        if not plot_image:
            logging.warning("Insufficient data to generate diversity plot")
            raise HTTPException(status_code=400, detail="Insufficient data to generate diversity plot.")
        logging.info(f"Generated plot for diversity: {plot_image[:100]}")
        return {"image": plot_image}
    except Exception as e:
        logging.error(f"Error generating diversity plot: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/plots/name_length")
async def get_name_length():
    try:
        if mongodb_client.db is None:
            logging.error("Database connection not established")
            raise HTTPException(status_code=500, detail="Database connection not established")

        logging.info("Loading data from MongoDB for name length plot")
        data = pd.DataFrame(list(mongodb_client.db["prenoms"].find({})))
        logging.info("Loaded data")
        plot_image = analyze_name_length(data)
        if not plot_image:
            logging.warning("Insufficient data to generate name length plot")
            raise HTTPException(status_code=400, detail="Insufficient data to generate name length plot.")
        logging.info(f"Generated plot for name length: {plot_image[:100]}")
        return {"image": plot_image}
    except Exception as e:
        logging.error(f"Error generating name length plot: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/plots/decade_analysis")
async def get_decade_analysis():
       try:
           if mongodb_client.db is None:
               logging.error("Database connection not established")
               raise HTTPException(status_code=500, detail="Database connection not established")

           logging.info("Loading data from MongoDB for decade analysis")
           data = pd.DataFrame(list(mongodb_client.db["prenoms"].find({})))
           logging.info("Loaded data")
           pivot_decade = analyze_by_decade(data)
           plot_image = measure_diversity(pivot_decade)
           if not plot_image:
               logging.warning("Insufficient data to generate decade analysis plot")
               raise HTTPException(status_code=400, detail="Insufficient data to generate decade analysis plot.")
           logging.info(f"Generated plot for decade analysis: {plot_image[:100]}")
           return {"image": plot_image}
       except Exception as e:
           logging.error(f"Error generating decade analysis plot: {e}")
           raise HTTPException(status_code=500, detail=str(e))
       
@router.get("/plots/geographic_diversity")
async def get_geographic_diversity():
       try:
           if mongodb_client.db is None:
               logging.error("Database connection not established")
               raise HTTPException(status_code=500, detail="Database connection not established")

           logging.info("Loading data from MongoDB for geographic diversity analysis")
           data = pd.DataFrame(list(mongodb_client.db["prenoms"].find({})))
           logging.info("Loaded data")
           plot_image = analyze_geographic_diversity(data)
           if not plot_image:
               logging.warning("Insufficient data to generate geographic diversity plot")
               raise HTTPException(status_code=400, detail="Insufficient data to generate geographic diversity plot.")
           logging.info(f"Generated plot for geographic diversity: {plot_image[:100]}")
           return {"image": plot_image}
       except Exception as e:
           logging.error(f"Error generating geographic diversity plot: {e}")
           raise HTTPException(status_code=500, detail=str(e))
       
@router.get("/plots/compound_names")
async def get_compound_names_analysis():
       try:
           if mongodb_client.db is None:
               logging.error("Database connection not established")
               raise HTTPException(status_code=500, detail="Database connection not established")

           logging.info("Loading data from MongoDB for compound names analysis")
           data = pd.DataFrame(list(mongodb_client.db["prenoms"].find({})))
           logging.info("Loaded data")
           plot_image = analyze_compound_names(data)
           if not plot_image:
               logging.warning("Insufficient data to generate compound names plot")
               raise HTTPException(status_code=400, detail="Insufficient data to generate compound names plot.")
           logging.info(f"Generated plot for compound names: {plot_image[:100]}")
           return {"image": plot_image}
       except Exception as e:
           logging.error(f"Error generating compound names plot: {e}")
           raise HTTPException(status_code=500, detail=str(e))