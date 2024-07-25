# Préparation des Données

## Étapes de Préparation des Données

### 1. Téléchargement et Chargement des Données

- Téléchargement du fichier `names.zip` contenant les données brutes.
- Extraction des fichiers de `names.zip` et chargement dans des DataFrames Pandas.

### 2. Exploration Initiale

- Calcul du nombre de naissances par sexe pour une année donnée (ex. 2000).
- Concaténation des données de toutes les années pour créer un ensemble de données complet.

### 3. Agrégation des Données

- Création de tableaux pivots pour représenter les naissances par année et par sexe.

### 4. Calcul des Proportions

- Ajout d'une colonne pour la proportion des naissances par prénom, sexe et année.
- Vérification de la somme des proportions pour chaque groupe (la somme doit être proche de 1).

### 5. Extraction des Sous-ensembles

- Extraction de sous-ensembles de 1000 prénoms les plus populaires par groupe avec une fonction spécifique.

## Documentation du Processus

- Documenter chaque étape du processus de préparation des données, y compris le code utilisé et les résultats obtenus.
- Tenir un journal des réunions, y compris les décisions prises et les tâches attribuées.
- Maintenir un plan de travail à jour, accessible à tous les membres de l'équipe.

## Téléchargement et Chargement des Données

- Les données sont téléchargées depuis `names.zip` et extraites dans le répertoire `data/`.
- Le script `load_data.py` est utilisé pour charger les données dans un DataFrame Pandas.

## Exploration Initiale

- Le nombre de naissances par sexe pour une année donnée est calculé à l'aide du script `exploration_initiale.py`.
- Les données de toutes les années sont concaténées pour créer un ensemble complet.

## Agrégation des Données

- Des tableaux pivots sont créés pour représenter les naissances par année et par sexe.

## Calcul des Proportions

- Une colonne est ajoutée pour la proportion des naissances par prénom, sexe et année.
- La somme des proportions pour chaque groupe est vérifiée pour s'assurer qu'elle est proche de 1.

## Extraction des Sous-ensembles

- Des sous-ensembles de 1000 prénoms les plus populaires par groupe sont extraits à l'aide de la fonction `extract_top_names` du script `exploration_initiale.py`.
