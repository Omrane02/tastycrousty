Readme · MD
# Ytasty Crousty
 
API backend pour la gestion de commandes de restauration rapide (restaurants, produits, commandes), développée avec FastAPI, PostgreSQL et une authentification JWT par rôles.
 
## Stack technique
 
- **FastAPI** — framework web et génération automatique de la documentation OpenAPI/Swagger
- **Pydantic** — validation des schémas d'entrée/sortie (`schema.py` par module)
- **PostgreSQL** — base de données relationnelle
- **SQLAlchemy (Core, sans ORM)** — exécution de requêtes SQL brutes via `text()` et `engine`
- **PyJWT** — génération et vérification des tokens d'authentification
- **bcrypt** — hachage des mots de passe
- **Docker / Docker Compose** — conteneurisation et démarrage en une seule commande
- **uv** — gestion des dépendances Python
## Structure du projet
 
```
src/
├── main.py                # point d'entrée, montage des routers, migration + seed au démarrage
├── core/
│   ├── security.py        # hash des mots de passe, création/décodage des tokens JWT
│   └── dependencies.py    # authentification, contrôle des rôles et des permissions par restaurant
├── db/
│   ├── config.py          # configuration (variables d'environnement)
│   ├── database.py        # connexion SQLAlchemy (engine)
│   ├── migration.sql      # définition des tables (CREATE TABLE)
│   ├── migration.py       # exécution du script de migration
│   └── seed.py             # insertion des données initiales (restaurants + compte admin)
└── modules/
    ├── auth/               # connexion (login) et émission du token
    ├── users/              # création des comptes utilisateurs
    ├── restaurants/        # consultation et gestion des restaurants
    ├── products/           # consultation et gestion des produits
    └── orders/             # création et suivi des commandes
```
 
## Prérequis
 
- Docker
- Docker Compose
Aucune installation Python locale n'est nécessaire : tout tourne dans les conteneurs.
 
## Installation et lancement en local
 
1. Cloner le dépôt :
```bash
   git clone <url-du-depot>
   cd tastycrousty
```
 
2. Créer le fichier `.env` à partir de l'exemple fourni :
```bash
   cp .env.example .env
```
 
   Puis renseigner les deux variables dans `.env` :
 
```
   SECRET_KEY=une_chaine_secrete_longue_et_aleatoire
   DATABASE_URL=postgresql+psycopg://ytasty:ytasty@db:5432/ytasty
```
 
   `SECRET_KEY` sert à signer les tokens JWT : elle doit être une chaîne longue et imprévisible (ne jamais utiliser une valeur simple en production). `DATABASE_URL` pointe vers le service `db` défini dans `docker-compose.yml` (utilisateur, mot de passe et nom de base doivent correspondre à ceux déclarés dans ce fichier).
 
3. Démarrer l'application :
```bash
   docker compose up --build
```
 
   Cette commande démarre deux services :
   - `db` : une base PostgreSQL (port `5432`)
   - `api` : l'application FastAPI (port `8000`)
   Au démarrage, l'application exécute automatiquement :
   - la migration (`migration.sql`), qui crée les tables si elles n'existent pas encore ;
   - le seed (`seed.py`), qui insère les données initiales si elles sont absentes.
4. Vérifier que tout fonctionne :
```
   http://localhost:8000/health
```
 
Pour réinitialiser complètement la base (tables et séquences) :
 
```bash
docker compose down -v
```
 
## Données pré-remplies
 
Au premier démarrage, l'application crée automatiquement :
 
**3 restaurants**
- Ytasty Crousty Aix
- Ytasty Crousty Lyon
- Ytasty Crousty Paris
**1 compte administrateur**
 
| Champ | Valeur |
|---|---|
| Nom d'utilisateur | `admin123` |
| Mot de passe | `Admin@123456` |
| Rôle | `admin` |
 
Ce compte permet de créer les autres utilisateurs (`staff`, `direction`) via `POST /users`.
 
## Documentation de l'API
 
Une fois l'application démarrée, la documentation interactive Swagger est disponible sur :
 
```
http://localhost:8000/docs
```
 
Le schéma OpenAPI brut est disponible sur :
 
```
http://localhost:8000/openapi.json
```
 
## Authentification
 
L'authentification se fait par JWT.
 
1. Récupérer un token via `POST /auth/login` avec `username` et `password` (compte admin pré-rempli ou tout compte créé) :
```bash
   curl -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin123", "password": "Admin@123456"}'
```
 
2. Utiliser le token reçu (`access_token`) dans l'en-tête `Authorization` des requêtes protégées :
```
   Authorization: Bearer <token>
```
 
   Dans Swagger, cliquer sur le bouton **Authorize** en haut de la page et coller le token (sans le préfixe `Bearer`, Swagger l'ajoute automatiquement).
 
### Rôles
 
| Rôle | Droits |
|---|---|
| `admin` | Accès complet à toutes les ressources, tous restaurants confondus |
| `staff` | Accès aux produits et commandes de son propre restaurant uniquement |
| `direction` | Consultation des restaurants ; consultation des commandes de tous les restaurants |
 
Un accès sans token renvoie `401 Unauthorized`. Un token valide mais un rôle insuffisant renvoie `403 Forbidden`.
 
## Endpoints principaux
 
| Méthode | Endpoint | Accès |
|---|---|---|
| `GET` | `/health` | public |
| `POST` | `/auth/login` | public |
| `POST` | `/users` | admin |
| `GET` | `/restaurants`, `/restaurants/{id}` | public |
| `PATCH` | `/restaurants/{id}`, `/restaurants/{id}/availability` | admin |
| `GET` | `/products` (filtres : `category`, `q`, `restaurant_id`, `is_available`) | public |
| `POST` / `PATCH` / `DELETE` | `/products` | admin, staff (son restaurant) |
| `POST` | `/orders` | public |
| `GET` | `/orders/{order_number}` | selon rôle |
| `GET` | `/restaurants/{restaurant_id}/orders` (filtre : `status`) | admin, direction (tous), staff (son restaurant) |
| `PATCH` | `/orders/{order_number}/status` | admin, direction, staff (son restaurant) |
| `POST` | `/orders/{order_number}/cancel` | admin, direction, staff (son restaurant) |
 
Le détail complet des paramètres et des schémas est disponible dans `/docs`.
 
## Déploiement
 
L'API est exposée publiquement via un tunnel ngrok :
 
```
https://frisk-array-lent.ngrok-free.dev
```
 
- Documentation Swagger publique : https://frisk-array-lent.ngrok-free.dev/docs
- Health check public : https://frisk-array-lent.ngrok-free.dev/health
> **Remarque** : le plan gratuit ngrok affiche une page d'avertissement intermédiaire tant que l'en-tête `ngrok-skip-browser-warning` n'est pas présent dans la requête. Pour tester l'API directement avec `curl` ou un client HTTP sans passer par un navigateur, ajouter cet en-tête :
>
> ```bash
> curl -H "ngrok-skip-browser-warning: true" https://frisk-array-lent.ngrok-free.dev/health
> ```
 
## Sécurité
 
- Aucun secret (clé JWT, identifiants de base de données) n'est versionné dans Git : ils sont définis dans `.env`, qui est ignoré par `.gitignore`. Un fichier `.env.example` documente les variables attendues sans valeurs réelles.
 


