from fastapi import APIRouter, HTTPException
import pandas as pd
import plotly.graph_objects as go  
from scripts.analysis import create_pivot_table, study_trends, measure_diversity, analyze_name_length, analyze_by_decade
from app.db import mongodb_client
import logging
import base64 

router = APIRouter()

@router.get("/plots/trends")
async def get_trends(names: str):
async def get_trends(name1: str = None, name2: str = None):
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
        logging.info(f"Data loaded. Sample: {data.head()}")
        pivot_table = create_pivot_table(data)
        logging.info(f"Pivot table created with columns: {pivot_table.columns.tolist()}")

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
        logging.info(f"Loaded data: {data.head()}")
        pivot_table = create_pivot_table(data)
        logging.info(f"Pivot table created with columns: {pivot_table.columns.tolist()}")
        plot_image = measure_diversity(pivot_table)
        if not plot_image:
            logging.warning("Insufficient data to generate diversity plot")
            raise HTTPException(status_code(400), detail="Insufficient data to generate diversity plot.")
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
        logging.info(f"Loaded data: {data.head()}")
        plot_image = analyze_name_length(data)
        if not plot_image:
            logging.warning("Insufficient data to generate name length plot")
            raise HTTPException(status_code(400), detail="Insufficient data to generate name length plot.")
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
        logging.info(f"Loaded data: {data.head()}")
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
    
@router.get("/plots/yearly_births")
async def get_yearly_births():
    try:
        if mongodb_client.db is None:
            logging.error("Database connection not established")
            raise HTTPException(status_code=500, detail="Database connection not established")

        logging.info("Loading data from MongoDB for yearly births plot")
        data = pd.DataFrame(list(mongodb_client.db["prenoms"].find({})))
        logging.info(f"Loaded data: {data.head()}")
        
        yearly_births = data.groupby('Year')['Count'].sum()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=yearly_births.index, y=yearly_births.values, mode='lines', name='Nombre de naissances'))
        fig.update_layout(title='Nombre de naissances par année', xaxis_title='Année', yaxis_title='Nombre de naissances')
        
        image_base64 = fig.to_image(format="png")
        return {"image": base64.b64encode(image_base64).decode('utf-8')}
    except Exception as e:
        logging.error(f"Error generating yearly births plot: {e}")
        raise HTTPException(status_code=500, detail=str(e))
