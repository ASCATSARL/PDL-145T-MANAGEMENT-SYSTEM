# GOUVERNIA - Système IA Gouvernementale RDC

## Vue d'ensemble

GOUVERNIA est un système modulaire d'intelligence artificielle conçu pour la gouvernance transparente et efficace en République Démocratique du Congo. Il intègre quatre modules principaux :

- **BudgetGuard** : Contrôle budgétaire et détection d'anomalies
- **InvestSmart** : Optimisation des investissements publics
- **TranspaFin** : Transparence financière et traçabilité blockchain
- **PeaceNet** : Sécurité et prévention des conflits

## Architecture

### Technologies utilisées

- **Backend** : Python 3.12, Flask, SQLAlchemy
- **Frontend** : HTML5, CSS3, JavaScript, Bootstrap 5
- **Base de données** : SQLite (développement local)
- **IA/ML** : Scikit-learn, Pandas, NumPy
- **Visualisation** : Chart.js, Plotly
- **CLI** : Click, Rich

### Structure du projet

```
gouvernia/
├── app.py                 # Application Flask principale
├── cli.py                # Interface CLI complète
├── simple_cli.py         # Interface CLI simplifiée
├── models.py             # Modèles de base de données
├── config.py             # Configuration de l'application
├── requirements.txt      # Dépendances Python
├── README.md            # Documentation
├── logs/                # Fichiers de log
├── templates/           # Templates HTML
│   ├── base.html        # Template de base
│   ├── dashboard.html   # Tableau de bord
│   ├── login.html       # Page de connexion
│   ├── budget.html      # Module BudgetGuard
│   ├── investments.html # Module InvestSmart
│   ├── transparency.html # Module TranspaFin
│   ├── security.html    # Module PeaceNet
│   └── error.html       # Page d'erreur
└── static/              # Fichiers statiques
    └── css/
        └── style.css    # Styles personnalisés
```

## Installation pour le développement local

### Prérequis

- Python 3.12 ou supérieur
- pip (gestionnaire de paquets Python)
- Git (optionnel)

### Étapes d'installation

1. **Cloner le projet**

   ```bash
   git clone [URL_DU_REPO]
   cd gouvernia
   ```

2. **Créer un environnement virtuel**

   ```bash
   python -m venv venv
   ```

3. **Activer l'environnement virtuel**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

5. **Initialiser la base de données SQLite**

   ```bash
   flask init-db
   flask seed-db
   ```

   Cela créera une base de données SQLite locale (`gouvernia.db`) avec des données de démonstration.

## Utilisation en développement local

### Lancement de l'application web

```bash
flask run
```

L'application sera accessible à l'adresse : http://localhost:5000

Vous pouvez également activer le mode de développement Flask avec :

```bash
flask --debug run
```

### Interface CLI

#### CLI complète

```bash
# Afficher l'aide
python cli.py --help

# Initialiser la base de données
python cli.py db-cmd init

# Insérer des données d'exemple
python cli.py db-cmd seed

# Afficher le tableau de bord
python cli.py report dashboard

# Gérer le budget
python cli.py budget status

# Gérer les investissements
python cli.py investment list

# Gérer la sécurité
python cli.py security alerts
```

#### CLI simplifiée (démonstration)

```bash
# Afficher le tableau de bord démo
python simple_cli.py dashboard

# Afficher les informations budgétaires
python simple_cli.py budget

# Afficher les investissements
python simple_cli.py investments

# Afficher les alertes de sécurité
python simple_cli.py security

# Exporter les données
python simple_cli.py export --export
```

### Identifiants de démonstration

- **Admin** : admin / admin123
- **Utilisateur** : demo / demo123

## Modules

### 1. BudgetGuard

- **Objectif** : Contrôle budgétaire et détection d'anomalies
- **Fonctionnalités** :
  - Suivi des dépenses par ministère et secteur
  - Détection automatique d'anomalies par IA
  - Alertes en cas de dépassement budgétaire
  - Rapports de conformité

### 2. InvestSmart

- **Objectif** : Optimisation des investissements publics
- **Fonctionnalités** :
  - Évaluation multi-critères des projets
  - Optimisation du portefeuille d'investissements
  - Suivi de la performance (ROI, efficacité)
  - Cartographie des projets

### 3. TranspaFin

- **Objectif** : Transparence financière et traçabilité
- **Fonctionnalités** :
  - Registre transparent des transactions
  - Traçabilité blockchain
  - Vérification d'intégrité
  - Rapports de transparence

### 4. PeaceNet

- **Objectif** : Sécurité et prévention des conflits
- **Fonctionnalités** :
  - Monitoring des tensions sociales
  - Cartographie des risques
  - Système d'alerte précoce
  - Analyse prédictive des conflits

## API REST

### Endpoints principaux

- `GET /api/budget-summary` - Résumé budgétaire
- `GET /api/investment-summary` - Résumé des investissements
- `GET /api/security-summary` - Résumé sécuritaire
- `GET /api/transparency-reports` - Rapports de transparence

## Configuration locale

### Configuration de développement

Tous les paramètres sont configurés dans `config.py` avec des valeurs par défaut adaptées au développement local :

- Base de données SQLite locale (`gouvernia.db`)
- Clé secrète de développement intégrée
- Configuration optimisée pour localhost
- Mode débug activé

### Personnalisation

Le fichier `config.py` permet de configurer :

- Les paramètres de la base de données SQLite
- Les seuils d'alerte IA
- Les paramètres de sécurité
- Les configurations spécifiques RDC

## Développement

### Structure des modèles

- **User** : Utilisateurs et authentification
- **Budget** : Budgets ministériels
- **Transaction** : Transactions financières
- **Investment** : Projets d'investissement
- **SecurityAlert** : Alertes de sécurité
- **TransparencyReport** : Rapports de transparence

### Tests

```bash
# Lancer les tests
python -m pytest tests/

# Tests de couverture
python -m pytest --cov=gouvernia tests/
```

## Contribution au développement

### Guide de contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Implémenter vos changements
4. Exécuter les tests pour vérifier que rien n'est cassé
   ```bash
   python -m pytest tests/
   ```
5. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
6. Push vers la branche (`git push origin feature/AmazingFeature`)
7. Ouvrir une Pull Request

### Environnement de développement

Pour travailler efficacement sur le projet :

1. **Activer le mode debug de Flask**

   ```bash
   flask --debug run
   ```

2. **Consulter les logs** dans le dossier `logs/`

3. **Base de données** : Le développement se fait avec SQLite. Vos changements seront stockés dans le fichier `gouvernia.db` local.

4. **Exécuter les tests**

   ```bash
   # Tests unitaires
   python -m pytest tests/

   # Avec couverture
   python -m pytest --cov=gouvernia tests/
   ```

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Support

Pour toute question ou problème, veuillez créer une issue sur GitHub ou contacter l'équipe de développement.

## Remerciements

- Équipe de développement GOUVERNIA
- Ministère des Finances RDC
- Partenaires techniques et institutionnels
