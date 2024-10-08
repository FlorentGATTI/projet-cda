import pandas as pd
from load_data import load_data

def main():
    data = load_data()

    year = 2000
    data_2000 = data[data['Year'] == year]
    births_by_sex = data_2000.groupby('Sex')['Count'].sum()
    print("Naissances par sexe pour l'année 2000:")
    print(births_by_sex)

    # Agrégation des données par année et par sexe
    pivot = data.pivot_table(values='Count', index='Year', columns='Sex', aggfunc='sum')
    print("\nTableau pivot des naissances par année et par sexe:")
    print(pivot.head())

    # Calcul des proportions
    data['TotalBirths'] = data.groupby(['Year', 'Sex'])['Count'].transform('sum')
    data['Proportion'] = data['Count'] / data['TotalBirths']

    # Vérification des proportions
    check = data.groupby(['Year', 'Sex'])['Proportion'].sum()
    print("\nVérification des proportions (la somme doit être proche de 1):")
    print(check.head())

    # Extraction des 1000 prénoms les plus populaires
    top_1000_names = extract_top_names(data)
    print("\nTop 5 des prénoms les plus populaires par groupe:")
    print(top_1000_names.head())

def extract_top_names(data, top_n=1000):
    grouped = data.groupby(['Year', 'Sex'], group_keys=False)
    top_names = grouped.apply(lambda x: x.nlargest(top_n, 'Count').reset_index(drop=True)).reset_index()
    return top_names[['Name', 'Sex', 'Count', 'Year', 'TotalBirths', 'Proportion']]

if __name__ == "__main__":
    main()
