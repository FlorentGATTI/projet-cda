from fastapi import APIRouter, HTTPException
from scripts.analysis import create_pivot_table, study_trends, measure_diversity, analyze_name_length
from scripts.load_data import load_data
import logging

router = APIRouter()

@router.get("/plots/trends")
async def get_trends(names: str):
    try:
        data = load_data()
        logging.info(f"Loaded data with names: {names}")
        pivot_table = create_pivot_table(data)
        logging.info(f"Pivot table data: {pivot_table.head()}")
        name_list = names.split(',')
        plot_image = study_trends(pivot_table, name_list)
        if not plot_image:
            raise HTTPException(status_code=400, detail="Insufficient data to generate trends plot.")
        logging.info(f"Generated plot for trends: {plot_image[:100]}")
        return {"image": plot_image}
    except Exception as e:
        logging.error(f"Error generating trends plot: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/plots/diversity")
async def get_diversity():
    try:
        data = load_data()
        logging.info("Loaded data")
        pivot_table = create_pivot_table(data)
        logging.info(f"Pivot table data: {pivot_table.head()}")
        plot_image = measure_diversity(pivot_table)
        if not plot_image:
            raise HTTPException(status_code=400, detail="Insufficient data to generate diversity plot.")
        logging.info(f"Generated plot for diversity: {plot_image[:100]}")
        return {"image": plot_image}
    except Exception as e:
        logging.error(f"Error generating diversity plot: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/plots/name_length")
async def get_name_length():
    try:
        data = load_data()
        logging.info("Loaded data")
        plot_image = analyze_name_length(data)
        if not plot_image:
            raise HTTPException(status_code=400, detail="Insufficient data to generate name length plot.")
        logging.info(f"Generated plot for name length: {plot_image[:100]}")
        return {"image": plot_image}
    except Exception as e:
        logging.error(f"Error generating name length plot: {e}")
        raise HTTPException(status_code=500, detail=str(e))
