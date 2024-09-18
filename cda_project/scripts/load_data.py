import os
import pandas as pd
from zipfile import ZipFile
from pymongo import MongoClient
import time
import logging

# Configuration de la journalisation
logging.basicConfig(level=logging.INFO)

def extract_zip_if_needed(zip_file, extract_to):
    if not os.path.exists(extract_to) or not os.listdir(extract_to):
        with ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            logging.info(f"Extracted {zip_file} to {extract_to}")
    else:
        logging.info(f"{zip_file} is already extracted.")

def load_names_data(data_dir):
    start_time = time.time()
    
    all_files = os.listdir(data_dir)
    # Ajout de la vérification isinstance(f, str)
    data_files = [f for f in all_files if isinstance(f, str) and f.startswith('yob') and f.endswith('.txt')]
    
    data_files = [f for f in all_files if f.startswith('yob') and f.endswith('.txt')]
    if not data_files:
        raise ValueError("No name data files found in the directory.")
    
    data_list = []
    for file in data_files:
        year = int(file[3:7])
        file_path = os.path.join(data_dir, file)
        df = pd.read_csv(file_path, names=['Name', 'Sex', 'Count'])
        df['Year'] = year
        data_list.append(df)

    if not data_list:
        raise ValueError("No valid data found in name data files.")

    data = pd.concat(data_list, ignore_index=True)
    logging.info(f"Loading names data took {time.time() - start_time:.2f} seconds")
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
def load_names_by_state_data(data_dir):
    start_time = time.time()
    
    state_files = os.listdir(data_dir)
    logging.info(f"Files found in {data_dir}: {state_files}")
    if not state_files:
        raise ValueError("No state data files found in the directory.")
    
    data_list = []
    for file in state_files:
        if file.endswith('.txt'):  # Only process .txt files
            file_path = os.path.join(data_dir, file)
            df = pd.read_csv(file_path, names=['State', 'Sex', 'Year', 'Name', 'Count'])
            data_list.append(df)

    if not data_list:
        raise ValueError("No valid data found in state data files.")

    data = pd.concat(data_list, ignore_index=True)
    logging.info(f"Loading names by state data took {time.time() - start_time:.2f} seconds")
    return data

def load_names_by_territory_data(data_dir):
    start_time = time.time()
    
    territory_files = os.listdir(data_dir)
    logging.info(f"Files found in {data_dir}: {territory_files}")
    if not territory_files:
        raise ValueError("No territory data files found in the directory.")
    
    data_list = []
    for file in territory_files:
        if file.endswith('.txt'):  # Only process .txt files
            file_path = os.path.join(data_dir, file)
            df = pd.read_csv(file_path, names=['Territory', 'Sex', 'Year', 'Name', 'Count'])
            data_list.append(df)

    if not data_list:
        raise ValueError("No valid data found in territory data files.")

    data = pd.concat(data_list, ignore_index=True)
    logging.info(f"Loading names by territory data took {time.time() - start_time:.2f} seconds")
    return data

def insert_data_to_mongodb(data, collection_name):
    start_time = time.time()
    
    client = MongoClient("mongodb://localhost:27017")
    db = client["cda"]
    collection = db[collection_name]

    # Utilisation de l'insertion en masse
    data_dict = data.to_dict("records")
    collection.insert_many(data_dict, ordered=False)
    
    client.close()
    logging.info(f"Inserting data into MongoDB collection {collection_name} took {time.time() - start_time:.2f} seconds")

def main():
    # Définir le chemin absolu pour le répertoire des données
    script_dir = os.path.dirname(__file__)
    data_dir = os.path.join(script_dir, '..', 'data')

    # Extraire les datasets si nécessaire
    extract_zip_if_needed(os.path.join(data_dir, "names.zip"), data_dir)
    extract_zip_if_needed(os.path.join(data_dir, "namesbystate.zip"), os.path.join(data_dir, "namesbystates"))
    extract_zip_if_needed(os.path.join(data_dir, "namesbyterritory.zip"), os.path.join(data_dir, "namesbyterritory"))

    # Charger et insérer les données des prénoms
    logging.info("Loading names data...")
    names_data = load_names_data(data_dir)
    insert_data_to_mongodb(names_data, "prenoms")

    # Charger et insérer les données des prénoms par état
    logging.info("Loading names by state data...")
    names_by_state_data = load_names_by_state_data(os.path.join(data_dir, 'namesbystates'))
    insert_data_to_mongodb(names_by_state_data, "names_by_state")

    # Charger et insérer les données des prénoms par territoire
    logging.info("Loading names by territory data...")
    names_by_territory_data = load_names_by_territory_data(os.path.join(data_dir, 'namesbyterritory'))
    insert_data_to_mongodb(names_by_territory_data, "names_by_territory")

    logging.info("All data has been successfully imported into MongoDB.")

if __name__ == "__main__":
    main()
