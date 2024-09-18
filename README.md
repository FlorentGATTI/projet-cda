# Projet d'Analyse des Prénoms des Bébés aux États-Unis

![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.85-green)

## Description

L'administration américaine de la sécurité sociale (SSA) a rendu publiques les données sur la fréquence des prénoms attribués aux bébés depuis 1880 jusqu'en 2018. Ce projet vise à analyser ces données pour identifier les tendances et les modèles dans l'attribution des prénoms. Une interface utilisateur est également développée pour présenter les résultats.

## Installation

Clonez le dépôt et installez les dépendances requises. Assurez-vous que votre version de Python est correcte (Python 3.12.4) :

```bash
git clone https://github.com/FlorentGATTI/projet-cda
cd cda_project
python -m venv env
source env/bin/activate  # Sur Windows: env\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```
MONGODB_URL=mongodb://localhost:27017
```

Vous pouvez adapter cette URL en fonction de votre environnement MongoDB.

## MongoDB

1. Créez une nouvelle base de données dans MongoDB appelée **cda**.
2. Créez une nouvelle collection **prenoms**.
3. Exécutez le script suivant pour charger les données dans la base de données MongoDB :

```bash
python scripts/load_data.py
```

## Préparation des données Mapbox

Pour préparer les données nécessaires à l'affichage de la carte interactive, vous devez exécuter le script `prepare_mapbox_data.py` qui génère des fichiers GeoJSON pour les prénoms par état et par territoire. Ce script se connecte à MongoDB et génère deux fichiers GeoJSON dans le répertoire `data/` :

```bash
python scripts/prepare_mapbox_data.py
```

## Structure du Projet

```bash
.
├── README.md
├── app
│   ├── crud
│   │   └── operations.py
│   ├── db.py
│   ├── main.py
│   ├── middlewares
│   │   └── cors.py
│   ├── models
│   │   ├── data.py
│   │   ├── geographic_diversity.py
│   │   └── prenoms.py
│   ├── routes
│   │   ├── data.py
│   │   ├── geographic_diversity.py
│   │   ├── plot.py
│   │   └── prenoms.py
│   ├── static
│   │   └── index.html
│   └── templates
│       └── index.html
├── data
│   ├── NationalReadMe.pdf
│   ├── names.zip
│   ├── names_by_state.geojson
│   ├── names_by_territory.geojson
│   ├── namesbystates
│   │   ├── AK.TXT
│   │   ├── AL.TXT
│   │   ├── CA.TXT
│   │   └── (autres fichiers .TXT des états)
│   ├── namesbyterritory
│   │   ├── PR.TXT
│   │   └── TR.TXT
│   └── stateTerritoryMappings.js
├── docs
│   ├── data_preparation.md
│   ├── meeting_notes.md
│   └── work_plan.md
├── env
│   ├── bin
│   ├── lib
│   └── share
├── frontend
│   ├── babel.config.js
│   ├── jsconfig.json
│   ├── package-lock.json
│   ├── package.json
│   ├── src
│   │   ├── App.vue
│   │   ├── components
│   │   ├── main.js
│   │   └── views
│   └── vue.config.js
├── notebooks
│   └── test.ipynb
├── requirements.txt
├── scripts
│   ├── analyses_specifiques.py
│   ├── analysis.py
│   ├── exploration_initiale.py
│   ├── load_data.py
│   └── prepare_mapbox_data.py
└── tests
```

## Démarrage du projet

### Backend

Pour démarrer le serveur backend FastAPI :

```bash
uvicorn app.main:app --reload
```

L’API sera disponible à l’adresse : `http://127.0.0.1:8000`.

### Frontend

Pour démarrer le frontend (après avoir installé les dépendances via npm) :

```bash
cd frontend
npm install
npm run serve
```

L’application front-end sera disponible à l’adresse : `http://localhost:8080`.

## Documentation API

Vous pouvez consulter la documentation de l'API :

- [Swagger UI](http://127.0.0.1:8000/docs)
- [Redoc](http://127.0.0.1:8000/redoc)

## Routes API

Voici les principales routes disponibles dans l'API :

- `GET /` : Read Index
- `GET /api` : Read Root
- `GET /api/top_names/{year}` : Récupère les prénoms les plus populaires pour une année
- `GET /api/names` : Récupère tous les prénoms
- `GET /api/total_births/{year}` : Récupère le nombre total de naissances par année
- `GET /api/births_by_sex/{year}` : Récupère les naissances par sexe
- `GET /api/plots/trends` : Récupère les tendances des prénoms
- `GET /api/plots/diversity` : Récupère l'analyse de la diversité des prénoms
- `GET /api/plots/name_length` : Analyse de la longueur des prénoms
- `GET /api/plots/decade_analysis` : Analyse par décennie
- `GET /api/plots/geographic_diversity` : Analyse de la diversité géographique
- `GET /api/plots/compound_names` : Analyse des prénoms composés
- `GET /api/distinct_names_states` : Récupère les noms distincts par état
- `GET /api/distinct_sexes` : Récupère les sexes distincts
- `GET /api/distinct_names_territories` : Récupère les noms distincts par territoire
- `GET /api/distinct_years_states` : Récupère les années distinctes par état
- `GET /api/distinct_years_territories` : Récupère les années distinctes par territoire
- `GET /api/distinct_states` : Récupère les états distincts
- `GET /api/distinct_territories` : Récupère les territoires distincts
- `GET /api/names_data` : Récupère les données complètes des prénoms

## Exécution des tests

Pour lancer les tests unitaires, exécutez la commande suivante :

```bash
pytest tests/
```

Cela lancera tous les tests définis dans le répertoire `tests/`.
