import os
import pandas as pd
from zipfile import ZipFile

def load_data():
    # Définir le chemin absolu pour le répertoire des données
    script_dir = os.path.dirname(__file__)
    data_dir = os.path.join(script_dir, '../', 'data')
    zip_file = os.path.join(data_dir, "names.zip")

    # Extraction des fichiers
    with ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(data_dir)

    # Chargement des données
    all_files = os.listdir(data_dir)
    data_files = [f for f in all_files if f.startswith('yob') and f.endswith('.txt')]
    data_list = []

    for file in data_files:
        year = int(file[3:7])
        file_path = os.path.join(data_dir, file)
        df = pd.read_csv(file_path, names=['Name', 'Sex', 'Count'])
        df['Year'] = year
        data_list.append(df)

    data = pd.concat(data_list, ignore_index=True)
    return data
