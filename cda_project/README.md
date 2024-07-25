# Projet d'Analyse des Prénoms des Bébés aux États-Unis

## Description

L'administration américaine de la sécurité sociale (USSSA ou SSA) a rendu publiques les données sur la fréquence des prénoms attribués aux bébés depuis 1880 jusqu'en 2018. Ce projet vise à analyser ces données pour identifier les tendances et les modèles dans l'attribution des prénoms. Une interface utilisateur est également développée pour présenter les résultats de vos données.

## Installation

Clonez le dépôt et installez les dépendances requises (!! Important vérifier sa version de python(3.12.4):

```bash
git clone https://github.com/FlorentGATTI/projet-cda
cd cda_project
python -m venv env
source env/bin/activate  # Sur Windows: env\Scripts\activate
pip install -r requirements.txt
```

## Structure du Projet

```ko
cda_project/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── requirements.txt
├── scripts/
│   ├── __pycache__/
│   │   └── load_data.cpython-311.pyc
│   ├── exploration_initiale.py
│   └── load_data.py
├── app/
│   ├── main.py
│   ├── routes/
│   │   ├── data.py
│   │   └── prenoms.py
│   ├── models/
│   │   ├── data.py
│   │   └── prenoms.py
│   ├── templates/
│   └── static/
├── tests/
├── .gitignore
├── README.md
└── venv/

```

## Utilisation

Pour charger les données et lancer l'analyse initiale :

```bash
python scripts/load_data.py
python scripts/exploration_initiale.py
python scripts/analyses_specifiques.py ## Ou voir notebooks/test.ipynb
```

Pour démarrer le serveur FastAPI :

```bash
uvicorn app.main:app --reload
```

## Documentation

La documentation de l'API est accessible via Swagger UI à l'adresse suivante :

```bash
http://127.0.0.1:8000/docs ## pour Swagger
http://127.0.0.1:8000/redoc ## pour Redoc
```

## Routes API

Voici les routes disponibles dans l'API :

#### **--*"/" # Retourne un message de bienvenue***

##### **Réponse :**

```json
{
  "message": "Bienvenue à l'API des prénoms des bébés aux États-Unis"
}
```

#### **--"/total\_births/ {year}"  # Retourne le nombre total de naissances pour une année donnée.**

##### Réponse :

```json
{
  "year": 1990,
  "total_births": 123456
}
```

#### -- "/top_names/ {year}" # Retourne les 1000 prénoms les plus populaires pour une année donnée.

##### **Réponse :**

```json
[
  {
    "name": "John",
    "count": 5000
  },
  {
    "name": "Jane",
    "count": 4800
  }
  ...
]
```

## Routes Back

```py
/ index

/total_births/{year}

/top_names/{year}
