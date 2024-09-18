import os
import pandas as pd
from zipfile import ZipFile
from pymongo import MongoClient

def load_data():
    # Définir le chemin absolu pour le répertoire des données
    script_dir = os.path.dirname(__file__)
    data_dir = os.path.join(script_dir, '..', 'data')
    zip_file = os.path.join(data_dir, "names.zip")

    # Extraction des fichiers
    with ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(data_dir)

    # Chargement des données
    all_files = os.listdir(data_dir)
    # Ajout de la vérification isinstance(f, str)
    data_files = [f for f in all_files if isinstance(f, str) and f.startswith('yob') and f.endswith('.txt')]
    
    if not data_files:
        raise ValueError("No name data files found in the directory.")
    
    data_list = []

    for file in data_files:
        year = int(file[3:7])
        file_path = os.path.join(data_dir, file)
        df = pd.read_csv(file_path, names=['Name', 'Sex', 'Count'])
        df['Year'] = year
        data_list.append(df)

    data = pd.concat(data_list, ignore_index=True)
    return data

def insert_data_to_mongodb(data):
    client = MongoClient("mongodb://localhost:27017")
    db = client["cda"]
    collection = db["prenoms"]

    data_dict = data.to_dict("records")
    collection.insert_many(data_dict)
    client.close()

if __name__ == "__main__":
    data = load_data()
    insert_data_to_mongodb(data)
    print("Data has been successfully imported into MongoDB.")