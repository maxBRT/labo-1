# Application de Gestion de Locations

Application de bureau développée avec Python et PySide6 pour gérer les locations d'équipements.

## Description

Cette application permet de gérer un système de location d'équipements avec les fonctionnalités suivantes :
- Gestion des clients
- Gestion des équipements
- Gestion des locations avec calcul automatique des coûts
- Suivi des retours d'équipements
- Recherche et filtrage des données

## Prérequis

- Python 3.13 ou supérieur
- [uv](https://docs.astral.sh/uv/).

### Installation de uv

Si `uv` n'est pas installé sur votre système :

**Sur macOS/Linux :**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Sur Windows (PowerShell) :**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Vérifier l'installation

```bash
uv --version
```

## Installation du projet

### Installer les dépendances

`uv` gère automatiquement l'environnement virtuel et les dépendances :

```bash
uv sync
```

Cette commande :
- Crée automatiquement un environnement virtuel
- Installe toutes les dépendances nécessaires (PySide6, SQLAlchemy, Pydantic)
- Configure le projet

## Initialisation de la base de données

Avant la première utilisation, générez des données de test :

```bash
uv run seed
```

Cette commande crée une base de données SQLite avec des exemples de clients, équipements et locations.

## Lancement de l'application

Une fois l'installation terminée, lancez l'application avec :

```bash
uv run main
```

L'interface graphique devrait s'ouvrir automatiquement.

## Utilisation de l'application

### Page Locations
- **Nouvelle location** : Créer une nouvelle location avec calcul automatique du coût total estimé
- **Marquer comme retourné** : Indiquer qu'un équipement a été retourné
- **Rechercher** : Filtrer les locations par nom de client ou d'équipement
- **Tri** : Cliquer sur les en-têtes de colonnes pour trier les données

### Page Clients
- Gérer la liste des clients
- Ajouter ou modifier des clients

### Page Équipements
- Gérer la liste des équipements disponibles
- Ajouter ou modifier des équipements

## Technologies utilisées

- **uv** : Gestionnaire de paquets et d'environnements moderne
- **PySide6** : Framework pour l'interface graphique 
- **SQLAlchemy** : ORM pour la gestion de la base de données
- **SQLite** : Base de données locale légère pour offrir une application completement hors-ligne
- **Pydantic** : Validation et sérialisation des données

## Résumé des commandes essentielles

```bash
# Installation des dépendances
uv sync

# Générer des données de test
uv run seed

# Lancer l'application
uv run main
```


*Projet développé dans le cadre d'un cours de développement d'application de bureau.*
