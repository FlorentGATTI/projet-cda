import pandas as pd
import plotly.graph_objects as go
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
    valid_names = [name for name in names if name in pivot_table.columns]
    if not valid_names:
        logging.warning("No valid names found in pivot table for trends plot.")
        return None
    logging.info(f"Using data for names: {valid_names}")
    logging.info(pivot_table[valid_names].head())
    
    fig = go.Figure()
    for name in valid_names:
        logging.info(f"Plotting data for {name}: {pivot_table[name].values}")
        fig.add_trace(go.Scatter(x=pivot_table.index, y=pivot_table[name], mode='lines', name=name))
    
    fig.update_layout(title='Tendances des prénoms', xaxis_title='Année', yaxis_title='Nombre de naissances')
    image_base64 = fig.to_image(format="png")
    logging.info("Trends plot created")
    return base64.b64encode(image_base64).decode('utf-8')

def measure_diversity(pivot_table):
    logging.info("Creating diversity plot")
    if pivot_table.empty:
        logging.warning("Pivot table is empty for diversity plot.")
        return None
    diversity = pivot_table.apply(entropy, axis=1)
    logging.info(f"Diversity data: {diversity.head()}")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=diversity.index, y=diversity, mode='lines', name='Diversité des prénoms'))
    
    fig.update_layout(title='Diversité des prénoms au fil des années', xaxis_title='Année', yaxis_title='Indice de Shannon')
    image_base64 = fig.to_image(format="png")
    logging.info("Diversity plot created")
    return base64.b64encode(image_base64).decode('utf-8')

def analyze_name_length(data):
    logging.info("Creating name length plot")
    if data.empty:
        logging.warning("Data is empty for name length plot.")
        return None
    data['NameLength'] = data['Name'].apply(len)
    length_trend = data.groupby('Year')['NameLength'].mean()
    logging.info(f"Name length data: {length_trend.head()}")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=length_trend.index, y=length_trend, mode='lines', name='Longueur moyenne des prénoms'))
    
    fig.update_layout(title='Tendance de la longueur des prénoms au fil des années', xaxis_title='Année', yaxis_title='Longueur moyenne des prénoms')
    image_base64 = fig.to_image(format="png")
    logging.info("Name length plot created")
    return base64.b64encode(image_base64).decode('utf-8')

def analyze_by_decade(data):
    data['Decade'] = (data['Year'] // 10) * 10
    pivot_decade = data.pivot_table(values='Count', index='Decade', columns='Name', aggfunc='sum', fill_value=0)
    return pivot_decade

def analyze_geographic_diversity(data):
    state_diversity = data.groupby(['State', 'Year'])['Name'].nunique()
    fig = go.Figure()
    for state in state_diversity.index.get_level_values('State').unique():
        fig.add_trace(go.Scatter(x=state_diversity[state].index, y=state_diversity[state].values, mode='lines', name=state))
    fig.update_layout(title='Diversity of first names by state over the years', xaxis_title='Year', yaxis_title='Number of unique first names')
    image_base64 = fig.to_image(format="png")
    return base64.b64encode(image_base64).decode('utf-8')

def analyze_compound_names(data):
    data['IsCompound'] = data['Name'].str.contains(' ')
    compound_trend = data.groupby('Year')['IsCompound'].mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=compound_trend.index, y=compound_trend.values, mode='lines', name='Proportion of compound first names'))
    fig.update_layout(title='Trends in compound names over the years', xaxis_title='Year', yaxis_title='Proportion of compound first names')
    image_base64 = fig.to_image(format="png")
    return base64.b64encode(image_base64).decode('utf-8')