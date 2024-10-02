import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy.stats import entropy
import base64

def create_pivot_table(data):
    return data.pivot_table(values='Count', index='Year', columns='Name', aggfunc='sum', fill_value=0)

def study_trends(pivot_table, name1, name2=None):
    names = [name for name in [name1, name2] if name and name in pivot_table.columns]
    if not names:
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
    
    fig = go.Figure()
    for name in names:
        fig.add_trace(go.Scatter(x=pivot_table.index, y=pivot_table[name], mode='lines', name=name))

    fig.update_layout(title='Tendances des prénoms', xaxis_title='Année', yaxis_title='Nombre de naissances')
    return fig

def measure_diversity(pivot_table):
    if pivot_table.empty:
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
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=diversity.index, y=diversity, mode='lines', name='Diversité des prénoms'))

    fig.update_layout(title='Diversité des prénoms au fil des années', xaxis_title='Année', yaxis_title='Indice de Shannon')
    return fig

def analyze_name_length(data):
    if data.empty:
        return None
    data['NameLength'] = data['Name'].str.len()
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
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=length_trend.index, y=length_trend, mode='lines', name='Longueur moyenne des prénoms'))

    fig.update_layout(title='Tendance de la longueur des prénoms au fil des années', xaxis_title='Année', yaxis_title='Longueur moyenne des prénoms')
    return fig

def analyze_by_decade(data):
    if data.empty:
        return None
    data['Decade'] = (data['Year'] // 10) * 10
    decade_data = data.groupby('Decade')['Count'].sum().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(x=decade_data['Decade'], y=decade_data['Count'], name='Naissances par décennie'))

    fig.update_layout(title='Analyse des naissances par décennie', xaxis_title='Décennie', yaxis_title='Nombre total de naissances')
    return fig

def analyze_geographic_diversity(data):
    state_diversity = data.groupby(['State', 'Year'])['Name'].nunique()
    fig = go.Figure()
    for state in state_diversity.index.get_level_values('State').unique():
        fig.add_trace(go.Scatter(x=state_diversity[state].index, y=state_diversity[state].values, mode='lines', name=state))
    fig.update_layout(title='Diversity of first names by state over the years', xaxis_title='Year', yaxis_title='Number of unique first names')
    image_base64 = fig.to_image(format="png")
    return base64.b64encode(image_base64).decode('utf-8')

def analyze_compound_names(data):
    if data.empty:
        return None
    data['IsCompound'] = data['Name'].str.contains(' ')
    compound_trend = data.groupby('Year')['IsCompound'].mean().reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=compound_trend['Year'], y=compound_trend['IsCompound'], mode='lines', name='Proportion of compound first names'))
    fig.update_layout(
        title='Trends in compound names over the years',
        xaxis_title='Year',
        yaxis_title='Proportion of compound first names'
    )
    return fig
