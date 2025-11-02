DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

-- TABLE DES UTILISATEURS (USERS)
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT NOT NULL UNIQUE, 
    email TEXT NOT NULL UNIQUE, 
    password TEXT NOT NULL, 
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
   
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,   
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

INSERT INTO users (username, email, password) VALUES
('alice_d', 'alice@example.com', 'hash_password_alice'),
('bob_w', 'bob@example.com', 'hash_password_bob'),
('charlie_p', 'charlie@example.com', 'hash_password_charlie'),
('david_s', 'david@example.com', 'hash_password_david'),
('eve_m', 'eve@example.com', 'hash_password_eve');

INSERT INTO posts (title, body, user_id) VALUES
(
  'Introduction à Flask', 
  'Flask est un micro-framework Python léger et puissant pour le développement web.', 
  1 
),
(
  'Maîtriser les bases de données SQL', 
  'Un guide pour comprendre les jointures, les clés étrangères et les index.', 
  2 
),
(
  'Le Clean Code en Python', 
  'Écrire du code lisible et maintenable est essentiel pour les projets à long terme.', 
  3
),
(
  'Débogage efficace avec VS Code', 
  'Comment utiliser les points d arrêts pour gagner du temps.', 
  4 
),
(
  'Déployer sur Heroku', 
  'Guide étape par étape pour mettre votre application Flask en ligne.', 
  5 
);


INSERT INTO comments (content, post_id, user_id) VALUES
(
  'Super article Alice ! Très clair.', 
  1, 
  2  
),
(
  'Je suis d accord, le Clean Code change la vie.', 
  3, 
  1  
),
(
  'Bonnes astuces sur le débogage David, merci.', 
  4,
  5  
),
(
  'J adore Flask, tellement simple à utiliser.', 
  1, 
  3  
),
(
  'Avez-vous essayé Argon2 pour le hachage des mots de passe ?', 
  2, 
  4 
);
