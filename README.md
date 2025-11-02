# 📚 Blog Moderne - Flask + React

Un système de blog complet avec authentification par session, articles et commentaires. Architecture client-serveur avec Flask API et interface React moderne.

**Auteur:** ADOSOSU Kévin

---

## 📋 Table des matières

- [Présentation](#-présentation)
- [Fonctionnalités](#-fonctionnalités)
- [Technologies](#-technologies)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Démarrage](#-démarrage)
- [Endpoints API](#-endpoints-api)
- [Guide d'utilisation](#-guide-dutilisation)
- [Structure du projet](#-structure-du-projet)

---

## 🎯 Présentation

**Blog Moderne** est une application web complète permettant aux utilisateurs de :
- Créer, lire, modifier et supprimer des articles
- Ajouter, modifier et supprimer des commentaires
- Gérer leurs profils
- Interagir avec la communauté

L'application utilise une **architecture moderne** avec séparation frontend/backend pour une meilleure scalabilité et maintenabilité.

### Points forts
✅ Authentification sécurisée par session  
✅ Interface réactive avec React  
✅ API REST documentée  
✅ Design moderne et responsive  
✅ Gestion complète des commentaires  
✅ Système de permissions robuste  

---

## ✨ Fonctionnalités

### 👤 Authentification
- ✅ Inscription avec validation email
- ✅ Connexion/Déconnexion sécurisée
- ✅ Sessions chiffrées
- ✅ Gestion de profil

### 📄 Articles
- ✅ Créer des articles
- ✅ Lire tous les articles publics
- ✅ Modifier ses articles
- ✅ Supprimer ses articles
- ✅ Voir ses articles personnels
- ✅ Vue Grille/Liste des articles

### 💬 Commentaires
- ✅ Ajouter des commentaires
- ✅ Lire les commentaires
- ✅ Modifier ses commentaires
- ✅ Supprimer ses commentaires
- ✅ Voir les infos auteur du commentaire

### 🎨 Interface
- ✅ Design moderne avec Tailwind CSS
- ✅ Mode responsive (mobile, tablet, desktop)
- ✅ Toggle Grille/Liste
- ✅ Animations fluides
- ✅ Système de couleurs cohérent (indigo)

---

## 🛠️ Technologies

### Backend (API)
| Technologie | Version | Usage |
|-------------|---------|-------|
| Python | 3.9+ | Langage principal |
| Flask | 2.x | Framework web |
| Flask-Login | - | Gestion des sessions |
| Flask-CORS | - | Cross-origin requests |
| SQLite | 3.x | Base de données |
| Werkzeug | - | Hashage des mots de passe |

### Frontend (Client)
| Technologie | Version | Usage |
|-------------|---------|-------|
| React | 18.x | Framework UI |
| Tailwind CSS | 3.x | Styling |
| Lucide React | - | Icônes |
| JavaScript ES6+ | - | Langage |

### Outils
- Git/GitHub - Versionning
- npm/pip - Gestionnaire de dépendances
- SQLite - Base de données locale

---

## 🏗️ Architecture

### Vue d'ensemble

```
┌─────────────────────────────────────────────────────────┐
│                    UTILISATEUR                          │
└─────────────────┬───────────────────────────────────────┘
                  │
                  |
    ┌───▼────────────┐  
    │  React (3000)  │  
    │  - HomePage    │  
    │  - Detail      │  
    │  - Auth        │  
    └───┬────────────┘  
        │                
        └─────────┬
                  │
        HTTP/REST │ Cookies
                  │
    ┌─────────────▼──────────────┐
    │  BACKEND API (Flask)       │
    │  (Port 5001)               │
    ├────────────────────────────┤
    │ Routes:                    │
    │ - /login                   │
    │ - /posts                   │
    │ - /comments                │
    │ - /users                   │
    └─────────────┬──────────────┘
                  │
                  │ SQL
                  │
    ┌─────────────▼──────────────┐
    │  BASE DE DONNÉES           │
    │  SQLite (flaskr.db)        │
    ├────────────────────────────┤
    │ - users                    │
    │ - posts                    │
    │ - comments                 │
    └────────────────────────────┘
```

### Flux de données

```
Login
  ↓
Générer Session
  ↓
Envoyer Cookie
  ↓
Requête + Cookie
  ↓
Vérifier Cookie
  ↓
Charger Utilisateur
  ↓
Traiter Requête
  ↓
Réponse JSON
```

---

## 📦 Installation

### Prérequis
- Python 3.9+
- pip et npm
- Git

### 1️⃣ Cloner le projet

```bash
git clone https://github.com/adososu/flask-blog.git
cd flask-blog
```

### 2️⃣ Installer le Backend

```bash
# Entrer dans le dossier API
cd api

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Créer le fichier .env
cp .env.example .env
```

### 3️⃣ Configurer l'API

Éditer `api/.env`:
```env
SECRET_KEY=your-super-secret-key-here-change-it
DATABASE_PATH=./flaskr.db
DEBUG=True
PORT=5001
FLASK_ENV=development
```

### 4️⃣ Installer le Frontend

```bash
# Revenir à la racine
cd ..

# Créer une app React (ou entrer dans un projet existant)
npx create-react-app client
cd client

# Installer Tailwind
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Installer les dépendances
npm install lucide-react
```

---

## 🚀 Démarrage

### Lancer l'API

```bash
cd api
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

python app.py
```

L'API démarre sur `http://localhost:5000`

```
 * Running on http://localhost:5001
 * Debug mode: on
```

### Lancer le Frontend

```bash
cd client
python app.py
```

L'app démarre sur `http://localhost:3000`

### Vérifier le fonctionnement

1. Aller sur `http://localhost:3000`
2. Créer un compte
3. Se connecter
4. Créer un article
5. Ajouter un commentaire

✅ Tout fonctionne !

---

## 📡 Endpoints API

### Authentification

#### `POST /register`
Créer un nouveau compte
```bash
curl -X POST http://localhost:5001/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "password": "Password123"
  }'
```
**Réponse (201):** `{ "success": true, "user_id": 1 }`

---

#### `POST /login`
Se connecter
```bash
curl -X POST http://localhost:5001/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "Password123"
  }'
```
**Réponse (200):**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com"
  }
}
```

---

#### `GET /logout`
Se déconnecter (protégé)
```bash
curl -X GET http://localhost:5001/logout \
  -b "session=xyz..."
```
**Réponse (200):** `{ "success": true }`

---

### Articles

#### `GET /posts`
Lister tous les articles
```bash
curl http://localhost:5001/posts
```
**Réponse (200):**
```json
{
  "success": true,
  "post": [
    {
      "id": 1,
      "title": "Mon article",
      "body": "Contenu...",
      "user_id": 1,
      "creationDate": "2025-10-26"
    }
  ]
}
```

---

#### `POST /posts`
Créer un article (protégé)
```bash
curl -X POST http://localhost:5001/posts \
  -H "Content-Type: application/json" \
  -b "session=xyz..." \
  -d '{
    "title": "Nouvel article",
    "body": "Contenu..."
  }'
```
**Réponse (201):** `{ "success": true, "post_id": 2 }`

---

#### `GET /posts/<id>`
Obtenir un article
```bash
curl http://localhost:5001/posts/1
```

---

#### `PUT /posts/<id>`
Modifier un article (propriétaire)
```bash
curl -X PUT http://localhost:5001/posts/1 \
  -H "Content-Type: application/json" \
  -b "session=xyz..." \
  -d '{
    "title": "Modifié",
    "body": "Nouveau contenu..."
  }'
```
**Réponse (200):** `{ "success": true }`

---

#### `DELETE /posts/<id>`
Supprimer un article (propriétaire)
```bash
curl -X DELETE http://localhost:5001/posts/1 \
  -b "session=xyz..."
```
**Réponse (200):** `{ "success": true }`

---

#### `GET /my-posts`
Lister mes articles (protégé)
```bash
curl http://localhost:5001/my-posts \
  -b "session=xyz..."
```

---

### Commentaires

#### `GET /posts/<post_id>/comments`
Lister les commentaires
```bash
curl http://localhost:5001/posts/1/comments
```
**Réponse (200):**
```json
{
  "success": true,
  "comments": [
    {
      "id": 1,
      "message": "Super!",
      "userId": 2,
      "username": "bob",
      "creationDate": "2025-10-26"
    }
  ]
}
```

---

#### `POST /posts/<post_id>/comments`
Ajouter un commentaire (protégé)
```bash
curl -X POST http://localhost:5001/posts/1/comments \
  -H "Content-Type: application/json" \
  -b "session=xyz..." \
  -d '{"message": "Excellent!"}'
```
**Réponse (201):** `{ "success": true, "comment_id": 5 }`

---

#### `PUT /comments/<id>`
Modifier un commentaire (propriétaire)
```bash
curl -X PUT http://localhost:5001/comments/1 \
  -H "Content-Type: application/json" \
  -b "session=xyz..." \
  -d '{"message": "Modifié..."}'
```
**Réponse (200):** `{ "success": true }`

---

#### `DELETE /comments/<id>`
Supprimer un commentaire (propriétaire)
```bash
curl -X DELETE http://localhost:5001/comments/1 \
  -b "session=xyz..."
```
**Réponse (200):** `{ "success": true }`

---

## 📋 Codes HTTP

| Code    | Signification                   |
|---------|---------------------------------|
| **200** | OK - Succès                     |
| **201** | Created - Ressource créée       |
| **400** | Bad Request - Données invalides |
| **401** | Unauthorized - Non connecté     |
| **403** | Forbidden - Non autorisé        |
| **404** | Not Found - Non trouvé          |
| **409** | Conflict - Existe déjà          |
| **500** | Server Error - Erreur serveur   |

---

## 📖 Guide d'utilisation

### Pour les utilisateurs

1. **S'inscrire**
   - Cliquer sur "S'inscrire"
   - Remplir le formulaire
   - Cliquer sur "Créer un compte"

2. **Se connecter**
   - Entrer email et mot de passe
   - Cliquer "Se connecter"

3. **Créer un article**
   - Remplir le formulaire (titre + contenu)
   - Cliquer "Publier"

4. **Commenter**
   - Aller sur un article
   - Écrire un commentaire
   - Cliquer "Envoyer"

5. **Gérer ses contenus**
   - Éditer/Supprimer ses articles et commentaires
   - Seul le propriétaire peut modifier

### Raccourcis

- `/ ` - Page d'accueil
- `/login` - Connexion
- `/register` - Inscription
- `/articles` - Mes articles
- `/articles/<id>` - Détail d'un article

---

## 📁 Structure du projet

```
flask-blog/
├── api/
│   ├── app.py                      # Application principale
│   ├── requirements.txt            # Dépendances Python
│   ├── .env.example               # Variables d'env (exemple)
│   ├── Config/
│   │   └── db.py                  # Configuration BD
│   ├── Controllers/
│   │   ├── usersController.py     # Gestion utilisateurs
│   │   ├── articlesController.py  # Gestion articles
│   │   └── commentsController.py  # Gestion commentaires
│   └── Models/
│       └── Model.py               # ORM personnalisé
│
├── client/
|   |   Controllers/
│   │   ├── usersController.py     # Gestion utilisateurs
│   │   ├── articlesController.py  # Gestion articles
│   │   └── commentsController.py  # Gestion commentaires
│   ├── Controllers
│   ├── Templates/
│   │   ├── css/   
│   │   ├── js/  
│   │   ├── img/cd 
│   │   ├── Layouts/
│   │   │   ├── default.html
│   │   │   ├── navbar.html
│   │   │── index.html
│   │   │── index.html
│   │   │── login.html
│   │   │── profil.html
│   │   │── my_articles.html
│   │   │── articles_detail.html
│   │   └── register.html
│   ├── package.json
│   └── app.py
│
├── README.md                      
├── .gitignore
└── LICENSE
```

---

## 🔒 Sécurité

### Authentification
- ✅ Sessions chiffrées avec SECRET_KEY
- ✅ Mots de passe hashés (Werkzeug)
- ✅ Cookies HttpOnly
- ✅ Protection CSRF (SameSite=Lax)

### Autorisation
- ✅ Vérification propriétaire pour éditer
- ✅ @login_required sur routes sensibles
- ✅ Validation des données côté serveur

### Bonnes pratiques
- ✅ SECRET_KEY longue et aléatoire
- ✅ .env pour les secrets
- ✅ CORS configuré
- ✅ Validation input

---

## 🐛 Troubleshooting

### "Connection refused" sur localhost:5001
- Vérifier que l'API est lancée: `python app.py`
- Vérifier le port dans `.env`

### "CORS error"
- Vérifier que CORS est activé dans `app.py`
- Vérifier l'origine dans `CORS(app, origins=[...])`

### "Database is locked"
- Fermer autres connexions SQLite
- Redémarrer l'API

### Session non persistée
- Vérifier que les cookies sont activés
- Vérifier `SECRET_KEY` en `.env`

---

## 📚 Ressources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Flask-Login](https://flask-login.readthedocs.io/)

---

## 📝 Licence

MIT - Libre d'utilisation

---

## 👨‍💻 Auteur

**ADOSOSU Kévin**

- GitHub: [@adososu](https://github.com/adososu)
- Email: kevin@example.com

---

## 🤝 Contribution

Les contributions sont bienvenues ! 

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request


**Dernière mise à jour:** 26 Octobre 2025