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
from app.db import get_cached_data, get_cached_pivot_table
import logging
import json

router = APIRouter()

def plot_to_json(fig):
    return json.loads(fig.to_json())
@router.get("/plots/trends")
async def get_trends(name1: str = None, name2: str = None):
    try:
        if mongodb_client.db is None:
            logging.error("Database connection not established")
            raise HTTPException(status_code=500, detail="Database connection not established")

        logging.info("Loading data from MongoDB for trends plot")
        data = pd.DataFrame(list(mongodb_client.db["prenoms"].find({})))
        logging.info(f"Loaded data with names: {name1}, {name2}")
        
        pivot_table = create_pivot_table(data)
        logging.info(f"Pivot table data: {pivot_table.head()}")

        names = []
        if name1:
            logging.info(f"Received name1: {name1}")
            names.append(name1)
        if name2:
            logging.info(f"Received name2: {name2}")
            names.append(name2)

        trends_data = {}
        for name in names:
            matching_columns = [col for col in pivot_table.columns if col == name]
            logging.info(f"Matching columns for {name}: {matching_columns}")
            if matching_columns:
                trends_data[matching_columns[0]] = pivot_table[matching_columns[0]].values
                logging.info(f"Data for {matching_columns[0]}: {trends_data[matching_columns[0]]}")
            else:
                logging.warning(f"Name {name} not found in the pivot table columns.")
                trends_data[name] = [0] * len(pivot_table.index)

        logging.info(f"Trends data prepared for plotting: {trends_data}")

        plot_image = study_trends(pivot_table, names)
        logging.info(f"Type of plot_image: {type(plot_image)}")
        logging.info(f"Content of plot_image: {plot_image[:100] if plot_image else None}")
        if not plot_image:
            logging.warning("Insufficient data to generate trends plot")
            return {"error": "Insufficient data to generate trends plot."}

        logging.info(f"Generated plot for trends: {plot_image[:100]}")
        return {"image": plot_image}
    except Exception as e:
        logging.error(f"Error generating trends plot: {e}")
        return {"error": str(e)}

@router.get("/plots/diversity")
def get_diversity_plot():
    try:
        pivot_table = get_cached_pivot_table()
        fig = measure_diversity(pivot_table)
        if fig is None:
            raise HTTPException(status_code=404, detail="No data available for diversity plot")
        return JSONResponse(content={"figure": plot_to_json(fig)})
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

@router.get("/plots/geographic_diversity")
def get_geographic_diversity_plot():
    try:
        data = get_cached_data()
        fig = analyze_geographic_diversity(data)
        if fig is None:
            raise HTTPException(status_code=404, detail="No data available for geographic diversity plot")
        return JSONResponse(content={"figure": plot_to_json(fig)})
        logging.info("Loading data from MongoDB for decade analysis")
        data = pd.DataFrame(list(mongodb_client.db["prenoms"].find({})))
        logging.info(f"Loaded data: {data.head()}")
        
        pivot_decade = analyze_by_decade(data)
        plot_image = measure_diversity(pivot_decade)
        if not plot_image:
            logging.warning("Insufficient data to generate decade analysis plot")
            raise HTTPException(status_code=400, detail="Insufficient data to generate decade analysis plot.")

        logging.info(f"Generated plot for decade analysis: {plot_image[:100]}")
        return {"image": plot_image}
    except Exception as e:
        logging.error(f"Error in get_geographic_diversity_plot: {str(e)}")
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
        logging.error(f"Error in get_compound_names_plot: {str(ve)}")
        raise HTTPException(status_code=500, detail=str(ve))
    except Exception as e:
        logging.error(f"Error in get_compound_names_plot: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while generating the compound names plot")

@router.get("/plots/trends")
def get_trends_plot(names: str = Query(..., description="Comma-separated list of names")):
    try:
        pivot_table = get_cached_pivot_table()
        name_list = [name.strip() for name in names.split(',') if name.strip()]
        if len(name_list) == 0:
            raise HTTPException(status_code=400, detail="At least one name must be provided")
        fig = study_trends(pivot_table, *name_list[:2])  # Unpack up to 2 names
        if fig is None:
            raise HTTPException(status_code=404, detail="No data available for the specified names")
        return JSONResponse(content={"figure": plot_to_json(fig)})
    except Exception as e:
        logging.error(f"Error in get_trends_plot: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while generating the trends plot")
        logging.error(f"Error generating yearly births plot: {e}")
        raise HTTPException(status_code=500, detail=str(e))