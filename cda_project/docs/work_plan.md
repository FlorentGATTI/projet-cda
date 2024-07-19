# Plan de Travail

## Organisations

### Membre A

**Responsabilités principales :**

- Acquisition et préparation des données
- Documentation et suivi du projet

**Tâches spécifiques :**

1. **Acquisition et Préparation des Données :**

   - Téléchargement et chargement des données depuis le fichier `names.zip`.
   - Exploration initiale : Calcul du nombre de naissances par sexe pour une année donnée et concaténation des données de toutes les années pour créer un ensemble complet.
   - Agrégation des données : Création de tableaux pivots pour représenter les naissances par année et par sexe.
   - Calcul des proportions : Ajout d'une colonne pour la proportion des naissances par prénom, sexe et année, et vérification de la somme des proportions pour chaque groupe.
   - Extraction des sous-ensembles : Extraction de sous-ensembles de 1000 prénoms les plus populaires par groupe avec une fonction spécifique.
2. **Documentation :**

   - Documenter chaque étape du processus de préparation des données.
   - Tenir à jour le suivi des réunions et le plan de travail partagé.

### Membre B

**Responsabilités principales :**

- Analyses spécifiques des données
- Développement de l'interface utilisateur avec FastAPI

**Tâches spécifiques :**

1. **Analyses Spécifiques :**

   - Création de tableaux pivots par prénom et année.
   - Étude des tendances : Analyse et représentation graphique des tendances de prénoms spécifiques comme "John" et "Harry".
   - Mesure de la diversité des prénoms.
   - Analyse par décennie et diversité géographique.
   - Analyse des tendances liées à la longueur des prénoms et des noms composés.
2. **Développement de l'Interface Utilisateur :**

   - Configuration de l'environnement de développement pour FastAPI.
   - Création des routes pour accès aux données.
   - Développement de l'interface utilisateur basique en respectant la charte graphique du SSA.

### Membre C

**Responsabilités principales :**

- Configuration et intégration de la base de données PostgreSQL
- Design et convivialité de l'interface utilisateur

**Tâches spécifiques :**

1. **Configuration de l'Environnement :**

   - Installation et configuration de PostgreSQL pour le stockage des données.
   - Intégration des données avec FastAPI.
2. **Développement de l'Interface Utilisateur :**

   - Conception intuitive : L'interface web est conçue pour offrir une expérience utilisateur intuitive et conviviale.
   - Création de fonctionnalités interactives : Sélection de prénoms, filtrage par année, et options de zoom et de défilement pour les graphiques interactifs.
   - Design et convivialité : S'assurer que l'interface est esthétique et conviviale.

## Plan d'Action Initial

1. **Organiser une Réunion Initiale :**

   - Discuter du projet, attribuer les tâches et répondre aux questions.
   - Utiliser un outil de gestion de projet pour suivre les tâches et les progrès (Trello, Jira, Asana, etc.).
2. **Préparer les Environnements de Développement :**

   - S'assurer que tous les membres ont accès aux outils nécessaires (Python, Pandas, FastAPI, PostgreSQL, etc.).
   - Configurer les environnements de développement pour tous les membres de l'équipe.
3. **Débuter avec l'Acquisition et la Préparation des Données :**

   - Membre A commence par télécharger et préparer les données en utilisant Pandas.
   - Membre B commence à explorer les analyses spécifiques des données.
   - Membre C installe et configure PostgreSQL, et commence à développer les premières fonctionnalités de l'interface utilisateur avec FastAPI.
