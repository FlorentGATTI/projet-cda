import pandas as pd
import plotly.graph_objects as go
from load_data import load_data
from scipy.stats import entropy

def create_pivot_table(data):
    # Crée un tableau pivot pour les prénoms par année
    pivot_table = data.pivot_table(values='Count', index='Year', columns='Name', aggfunc='sum', fill_value=0)
    return pivot_table

def study_trends(pivot_table, names):
    # Analyse et visualisation des tendances de prénoms spécifiques
    for name in names:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=pivot_table.index, y=pivot_table[name], mode='lines', name=name))
        fig.update_layout(title=f'Tendance du prénom {name}', xaxis_title='Année', yaxis_title='Nombre de naissances')
        fig.show()

def measure_diversity(pivot_table):
    # Calcul et visualisation de l'indice de diversité de Shannon pour chaque année
    diversity = pivot_table.apply(entropy, axis=1)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=diversity.index, y=diversity, mode='lines', name='Diversité des prénoms'))
    fig.update_layout(title='Diversité des prénoms au fil des années', xaxis_title='Année', yaxis_title='Indice de Shannon')
    fig.show()

def analyze_by_decade(data):
    # Ajoute une colonne 'Decade' au DataFrame et crée un tableau pivot par décennie
    data['Decade'] = (data['Year'] // 10) * 10
    pivot_decade = data.pivot_table(values='Count', index='Decade', columns='Name', aggfunc='sum', fill_value=0)
    return pivot_decade

def analyze_name_length(data):
    # Ajoute une colonne 'NameLength' au DataFrame et analyse la tendance de la longueur des prénoms
    data['NameLength'] = data['Name'].apply(len)
    length_trend = data.groupby('Year')['NameLength'].mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=length_trend.index, y=length_trend, mode='lines', name='Longueur moyenne des prénoms'))
    fig.update_layout(title='Tendance de la longueur des prénoms au fil des années', xaxis_title='Année', yaxis_title='Longueur moyenne des prénoms')
    fig.show()

def main():
    # Fonction principale pour exécuter les différentes analyses

    # Chargement des données
    data = load_data()

    # Création du tableau pivot par prénom et année
    pivot_table = create_pivot_table(data)
    
    # Étude des tendances pour les prénoms spécifiques
    study_trends(pivot_table, ['John', 'Harry'])

    # Mesure de la diversité des prénoms
    measure_diversity(pivot_table)

    # Analyse des données par décennie et mesure de la diversité par décennie
    pivot_decade = analyze_by_decade(data)
    measure_diversity(pivot_decade)

    # Analyse de la tendance de la longueur des prénoms
    analyze_name_length(data)

if __name__ == "__main__":
    # Exécution de la fonction principale si le script est exécuté directement
    main()