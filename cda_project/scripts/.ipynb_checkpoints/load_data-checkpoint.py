import pandas as pd
import os
from zipfile import ZipFile

def load_data():
    data_dir = "../data"
    zip_file = os.path.join(data_dir, "names.zip")

    # Extraction des fichiers
    with ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(data_dir)

    # Chargement des données
    all_data = []
    for file_name in os.listdir(data_dir):
        if file_name.startswith("yob"):
            year = int(file_name[3:7])
            df = pd.read_csv(os.path.join(data_dir, file_name), names=["Name", "Sex", "Count"])
            df['Year'] = year
            all_data.append(df)

    # Concatenation de toutes les années
    data = pd.concat(all_data, ignore_index=True)
    return data

if __name__ == "__main__":
    data = load_data()
    print(data.head())
