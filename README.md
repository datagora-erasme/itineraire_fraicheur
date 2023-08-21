# Sortons au frais

---

# Table des matières

- [À propos](#à-propos)
- [Pré-requis](#pré-requis)
- [Application web](#application-web)
    - [Backend](#backend)
    - [Frontend](#frontend)
- [Analyse statistique : pondération du réseau piéton](#analyse-statistique--pondération-du-réseau-piéton)

# À propos

Le projet Sortons au frais est un projet mené par Erasme (laboratoire d'innovation de la Métropole de Lyon) et le service géomatique de la métropole de Lyon. Ce projet a été réalisé en partenariat avec les services géomatiques d'une quinzaine de communes de la métropole de Lyon dans le cadre du projet OpenData. 
L'objectif est d'apporter une solution d'adaptation à la canicule en proposant une application ayant 3 fonctionnalitées principales. 

- Proposer des itinéraires piétons permettant de se déplacer "au frais".
- Trouver les lieux "frais" autour de chez soi
- Afficher des éléments utiles en cas de canicule (fontaines, parcs, toilettes etc.)

La totalité du code et de l'analyse statistique a été réalisé dans le cadre d'un stage de master 2 par Yannis BARBA et a donné lieu à un rapport de stage expliquant la démarche suivie pour déterminer la pondération du réseau piéton.
La partie statistique est présente dans le backend de l'application web mais le détail de l'arborescence des scripts est expliqué dans la partie [**Analyse statistique**](#analyse-statistique--pondération-du-réseau-piéton).

# Pré-requis et Insallation

Le projet a été développé dans un environnement conda, si l'application n'est pas exécutée via les images dockers, il est préférable de créer un environnement conda. Les versions utilisées dans le cadre de ce projet sont les suivantes : 

- **conda** : 23.1.0
- **docker** :  23.0.2
- **docker-compose** : 1.29.2

## Exécution via Docker

Les images docker du frontend et du backend sont disponibles à aux adresses suivantes : 
- backend : https://hub.docker.com/repository/docker/yannisbarba/itineraires_fraicheur_backend/general
- frontend : https://hub.docker.com/repository/docker/yannisbarba/itineraires_fraicheur_frontend/general

Une fois le projet téléchargé via github, se placer à la racine du projet et exécuter le fichier **docker-compose.yml** avec la commande :

```bash
    docker-compose build
```

Une fois le build réalisé, exécuter les images : 

```bash
    docker-compose up
```

## Exécution via conda (conseillé pour le développement)

### Création de l'environnement conda

Une fois conda installé (via anaconda par exemple), créer un environnement conda pour le projet via la commande suivante : 

```bash
    conda create --name <sortons-au-frais>
```
Suivre les indications de créations de l'environnement puis une fois à la racine du projet, activer l'environnement conda : 

```bash
    conda activate <sortons-au-frais>
```

Une fois l'environnement activé et avant de pouvoir exécuter le projet, se placer à la racine du projet lancer l'installation des dépendances : 

```bash
    pip install requirements.txt
```

## Exécution du backend
**Se placer à la racine du dossier backend**

Afin de lancer le backend, se positionner à la racine du dossier backend et exécuter la commande suivante : 

```bash
    python app.py

```

## Exécution du frontend
**Se placer à la racine du dossier frontend**

Avant de lancer l'exécution du frontend, il est nécessaire d'installer les dépendances npm via la commande : 

```bash
    npm install
```

Afin de lancer le frontend, exécuter la commande suivante : 

```bash
    npm start
```



# Application web

## Backend


Toutes les variables globales (les chemins des fichiers, les paramètres spécifiques etc.) sont stockées dans le fichier **global_variable.py** à la racine du dossier backend. Il n'y a pas de base de données pour ce projet car il n'y en avait pas le besoin. Les quelques informations nécessaires au bon fonctionnement du frontend (chemin des layers, chemin des icons etc.) sont également stockés directement dans un dictionnaire python dans le fichier **global_variable.py**.

Le backend est structuré en deux parties principales, l'API développée avec le framework **Flask** et les données avec l'analyse statistique (détaillée [ici](#analyse-statistique--pondération-du-réseau-piéton)).

### LES DONNÉES 
L'ensemble des données utiles pour l'application web (et pour le calcul de score) sont stockées dans le dossier *score_calculation_it/input_data*

On peut distinguer deux types de données : 

- Les [données](#requête-wfs) directement issues d'une requête WFS à l'api de datagrandlyon
- Les données de plus grosse taille et nécessitant des calculs spécifiques

#### Requête WFS

Les données issues d'une requête WFS à datagrandlyon peuvent être téléchargées directement en exécutant le script **fetch_data.py** situé dans le dossier *score_calculation_it/input_data/*. Il est possible de télécharger une donnée en particulier ou toutes les données d'un coup.  Afin de lancer le téléchargement, exécuter le script dans un terminal **en se plaçant au niveau du script** puis lancer la commande suivante : 

```bash
    python fetch_data.py
```
Puis se laisser guider par les indications dans le terminal.

À chaque fois qu'une donnée est téléchargée, un dossier se créé avec la donnée sous format geojson (pour l'affichage sur la web app) et sous format gpkg (pour l'ensemble des calculs). 

#### Autre données
Les autres données de taille trop importante et/ou nécessitant de trop gros calculs sont des données qui ne sont pas accessibles par l'utilisateur via l'application. 

##### La végétation
La donnée de végétation stratifiée la donnée la plus volumineuse. Il est possible de la recalculer de A à Z en partant de la donnée brute présente à [cette addresse](https://data.grandlyon.com/portail/fr/jeux-de-donnees/vegetation-stratifiee-2018-metropole-lyon/telechargements). Afin de pouvoir l'utiliser dans le cadre de ce projet, des calculs ont été réalisés avec Qgis.
- Réduire la résolution du raster (de 1m à 5m). 
- Vectoriser le raster
- réduire le nombre de classes (de 5 à 3). Les nouvelles classes sont : 
    - arbres (>1.5m)
    - arbustes (<1.5m)
    - prairies (anciennement herbacées)
Les temps de calculs sont relativement longs et demandent une RAM assez importante (> 16G).
Sauvegarder le résultat sous format Geopackage (gpkg). 

Sinon, la donnée déjà calculée est présente à [cette adresse](mettreadresse)
Une fois téléchargée, la donné de végétation doit être sauvegardée ici : *"./score_calculation_it/input_data/vegetation/raw_veget_strat.gpkg"*
Cette donnée étant encore trop volumineuse pour être manipulée aisément dans le cadre du projet, elle a été "clippé" avec la version bufferisée du réseau OSM. Le calcul étant long (24h !) avec une configuration standard, la version déjà calculée en date du 03.07.23 est présente [ici](mettreaddresse).
Pour mettre à jour cette donnée, exécuter le script **vegetation_preprocessing.py**. en se plaçant ici *./score_calculation_it/* et se laisser guider par les indications du terminal.

```bash
    python vegetation_preprocessing.py
```

##### La température

La donnée de température est également une donnée demandant des pré-calculs spécifiques. Le tutoriel pour recalculer cette donnée est disponible [ici](mettreaddresse).
La donnée déjà calculée est disponible à [cette adresse](mettreaddresse). Une fois téléchargée, elle doit être sauvegardée ici : *"./score_calculation_it/input_data/temperature/temperature_surface.gpkg"*.
Pour relancer le calcul de la température moyenne par segment, exécuter le script **temperature_preprocessing.py**en se plaçant ici *./score_calculation_it/* et suivre les indications du terminal.

```bash
    python temperature_preprocessing.py
```

### L'API
Le script python principal du backend est le fichier **app.py** qui constitue le *endpoint* du backend permettant d'exécuter les différentes requêtes utilisateur. Avant le lancement de l'application, vérifier que le chemin du graph est celui souhaité dans le fichier **global_variable.py**.

Il y a seulement deux routes:
- requête des layers
- requête pour le calcul d'itinéraire

Les endpoints se servent de fonction présentes dans le dossier *models* avec un fichier correspondant à chaque route.
Les données distribuées pour l'application web sont celles stockées dans le dossier *score_calculation_it/input_data/* (cf [partie](#les-données))



## Frontend

# Analyse statistique : pondération du réseau piéton
