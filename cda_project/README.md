# Projet d'Analyse des Prénoms des Bébés aux États-Unis

## Description

L'administration américaine de la sécurité sociale (USSSA ou SSA) a rendu publiques les données sur la fréquence des prénoms attribués aux bébés depuis 1880 jusqu'en 2018. Ce projet vise à analyser ces données pour identifier les tendances et les modèles dans l'attribution des prénoms.
Une interface utilisateur sera développée pour présenter les résultats de vos données.

## Installation

```
git clone https://github.com/FlorentGATTI/projet-cda
cd cda_project
python -m venv env
source env/bin/activate  # Sur Windows: env\Scripts\activate
pip install -r requirements.txt
```

## Structure du Projet

```\plaintext
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
│   │   └── prenoms.py
│   ├── models/
│   │   └── prenoms.py
│   ├── templates/
│   └── static/
├── tests/
├── .gitignore
├── README.md
└── venv/
```

## Utilisation

```python
python scripts/load_data.py

python scripts/exploration_initiale.pymermaid
```
