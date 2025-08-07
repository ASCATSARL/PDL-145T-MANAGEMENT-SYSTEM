# Guide de contribution - GOUVERNIA

## Aperçu du projet

GOUVERNIA est un système modulaire d'intelligence artificielle pour la gouvernance transparente en République Démocratique du Congo. Le développement se fait entièrement en local avec SQLite et Flask.

## Configuration de l'environnement de développement

### Prérequis

- Python 3.12 ou supérieur
- pip (gestionnaire de paquets Python)
- Git

### Installation initiale

1. **Cloner le projet**

   ```bash
   git clone [URL_DU_REPO]
   cd gouvernia
   ```

2. **Créer et activer un environnement virtuel**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

3. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

4. **Initialiser la base de données SQLite**
   ```bash
   flask init-db
   flask seed-db
   ```

## Workflow de développement

### Démarrage du serveur de développement

```bash
# Mode développement avec rechargement automatique
flask --debug run

# Ou simplement
flask run
```

L'application sera disponible sur http://localhost:5000

### Structure de la base de données

Le projet utilise SQLite pour le développement local :

- **Fichier de base de données** : `gouvernia.db` (créé automatiquement)
- **Modèles** : Définis dans `models.py`
- **Configuration** : `config.py` (classe `DevConfig`)

### Commandes Flask CLI utiles

```bash
# Initialiser la base de données
flask init-db

# Peupler avec des données de démonstration
flask seed-db

# Accéder au shell Flask avec contexte
flask shell
```

## Développement des fonctionnalités

### Architecture des modules

Le système est composé de 4 modules principaux :

1. **BudgetGuard** : Contrôle budgétaire et détection d'anomalies
2. **InvestSmart** : Optimisation des investissements publics
3. **TranspaFin** : Transparence financière et traçabilité
4. **PeaceNet** : Sécurité et prévention des conflits

### Ajout d'une nouvelle fonctionnalité

1. **Créer une branche**

   ```bash
   git checkout -b feature/nom-de-la-fonctionnalite
   ```

2. **Développer la fonctionnalité**
   - Ajouter les routes dans `app.py`
   - Créer/modifier les modèles dans `models.py`
   - Ajouter les templates HTML dans `templates/`
   - Ajouter les styles CSS dans `static/css/`

3. **Tester localement**

   ```bash
   flask --debug run
   ```

4. **Exécuter les tests**
   ```bash
   python -m pytest tests/
   ```

### Modification des modèles de données

Si vous modifiez la structure de la base de données :

1. Modifier les modèles dans `models.py`
2. Supprimer l'ancienne base de données :
   ```bash
   rm gouvernia.db
   ```
3. Recréer la base de données :
   ```bash
   flask init-db
   flask seed-db
   ```

## Tests et qualité du code

### Exécution des tests

```bash
# Tests unitaires
python -m pytest tests/

# Tests avec couverture
python -m pytest --cov=gouvernia tests/

# Tests avec sortie détaillée
python -m pytest -v tests/
```

### Débogage

1. **Logs** : Consultez les logs dans le dossier `logs/`
2. **Mode debug** : Utilisez `flask --debug run` pour le rechargement automatique
3. **Shell Flask** : `flask shell` pour interagir avec l'application

## Standards de code

### Structure des fichiers

- **Routes** : Organisées par module dans `app.py`
- **Modèles** : Un modèle par entité métier dans `models.py`
- **Templates** : HTML avec Bootstrap 5 dans `templates/`
- **Styles** : CSS personnalisés dans `static/css/style.css`

### Convention de nommage

- **Routes** : `/module/action` (ex: `/budget/anomalies`)
- **Templates** : `module_action.html` (ex: `budget_anomalies.html`)
- **Fonctions** : snake_case
- **Classes** : PascalCase

## Soumission des contributions

### Processus de pull request

1. **Finaliser votre travail**

   ```bash
   git add .
   git commit -m "feat: description concise de la fonctionnalité"
   ```

2. **Pousser votre branche**

   ```bash
   git push origin feature/nom-de-la-fonctionnalite
   ```

3. **Créer une pull request** avec :
   - Description claire des changements
   - Captures d'écran si interface utilisateur
   - Tests effectués
   - Impact sur les autres modules

### Format des messages de commit

Utilisez le format conventional commits :

- `feat:` nouvelle fonctionnalité
- `fix:` correction de bug
- `docs:` mise à jour documentation
- `style:` formatage, pas de changement de code
- `refactor:` refactoring de code
- `test:` ajout ou modification de tests

## Données de test

### Utilisateurs de démonstration

- **Admin** : `admin` / `admin123`
- **Utilisateur** : `demo` / `demo123`

### Commande seed-db

La commande `flask seed-db` crée automatiquement :

- Utilisateurs de test
- Budgets d'exemple pour différents ministères
- Projets d'investissement fictifs
- Alertes de sécurité de démonstration

## Ressources utiles

### Documentation technique

- **Flask** : https://flask.palletsprojects.com/
- **SQLAlchemy** : https://docs.sqlalchemy.org/
- **Bootstrap 5** : https://getbootstrap.com/docs/5.3/

### Configuration locale

Tous les paramètres de développement sont dans `config.py` :

- Base de données SQLite (`gouvernia.db`)
- Mode debug activé
- Logs détaillés
- Configuration simplifiée pour localhost

## Support

Pour toute question sur le développement :

1. Consultez cette documentation
2. Vérifiez les issues existantes sur GitHub
3. Créez une nouvelle issue si nécessaire
4. Contactez l'équipe de développement

## Sécurité

⚠️ **Important** : Cette configuration est uniquement pour le développement local. Ne jamais utiliser ces paramètres en production.
