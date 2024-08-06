import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import entropy
from io import BytesIO
import base64
import logging

def create_pivot_table(data):
    logging.info("Creating pivot table")
    pivot_table = data.pivot_table(values='Count', index='Year', columns='Name', aggfunc='sum', fill_value=0)
    logging.info(f"Pivot table created with columns: {pivot_table.columns}")
    return pivot_table

def study_trends(pivot_table, names):
    logging.info(f"Creating trends plot for names: {names}")
    plt.figure(figsize=(10, 6))
    valid_names = [name for name in names if name in pivot_table.columns]
    if not valid_names:
        logging.warning("No valid names found in pivot table for trends plot.")
        return None
    logging.info(f"Using data for names: {valid_names}")
    logging.info(pivot_table[valid_names].head())
    for name in valid_names:
        logging.info(f"Plotting data for {name}: {pivot_table[name].values}")
        plt.plot(pivot_table.index, pivot_table[name], label=name)
    plt.title('Tendances des prénoms')
    plt.xlabel('Année')
    plt.ylabel('Nombre de naissances')
    plt.legend()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    logging.info("Trends plot created")
    return image_base64

def measure_diversity(pivot_table):
    logging.info("Creating diversity plot")
    if pivot_table.empty:
        logging.warning("Pivot table is empty for diversity plot.")
        return None
    diversity = pivot_table.apply(entropy, axis=1)
    logging.info(f"Diversity data: {diversity.head()}")
    plt.figure(figsize=(10, 6))
    plt.plot(diversity.index, diversity, label='Diversité des prénoms')
    plt.title('Diversité des prénoms au fil des années')
    plt.xlabel('Année')
    plt.ylabel('Indice de Shannon')
    plt.legend()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    logging.info("Diversity plot created")
    return image_base64

def analyze_name_length(data):
    logging.info("Creating name length plot")
    if data.empty:
        logging.warning("Data is empty for name length plot.")
        return None
    data['NameLength'] = data['Name'].apply(len)
    length_trend = data.groupby('Year')['NameLength'].mean()
    logging.info(f"Name length data: {length_trend.head()}")
    plt.figure(figsize=(10, 6))
    logging.info(f"Plotting name length data: {length_trend.values}")
    plt.plot(length_trend.index, length_trend, label='Longueur moyenne des prénoms')
    plt.title('Tendance de la longueur des prénoms au fil des années')
    plt.xlabel('Année')
    plt.ylabel('Longueur moyenne des prénoms')
    plt.legend()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    logging.info("Name length plot created")
    return image_base64