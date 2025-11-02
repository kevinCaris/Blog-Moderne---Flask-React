from flask import request, session
import sqlite3
import re
from Models.Model import Model
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)

# ===== MODÈLE USER =====
class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

class UserController:
    
    @staticmethod
    def get_request_data():
        if request.is_json:
            return request.get_json()
        else:
            return request.form.to_dict()
    
    @staticmethod
    def validate_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            return False, 'Le mot de passe doit contenir au moins 8 caractères.'
        return True, 'OK'
    
    @staticmethod
    def register():
        data = UserController.get_request_data()
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not email or not password:
            return {
                'success': False,
                'message': 'Username, email et password sont requis.'
            }, 400
        
        if len(username) < 3:
            return {
                'success': False,
                'message': 'Le username doit contenir au moins 3 caractères.'
            }, 400
        
        if not UserController.validate_email(email):
            return {
                'success': False,
                'message': 'Format d\'email invalide.'
            }, 400
        
        is_valid, msg = UserController.validate_password(password)
        if not is_valid:
            return {
                'success': False,
                'message': msg
            }, 400
            
        hashed_password = generate_password_hash(password)
        
        try:
            user_data = {
                "username": username,
                "email": email,
                "password": hashed_password 
            }
            
            new_id = Model.create('users', user_data)
        
            return {
                'success': True,
                'message': 'Inscription réussie ! Vous pouvez maintenant vous connecter.',
                'user_id': new_id 
            }, 201
        except sqlite3.IntegrityError:
            return {
                'success': False,
                'message': 'Ce nom d\'utilisateur ou email existe déjà.'
            }, 409
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de l\'inscription: {str(e)}'
            }, 500
    
    @staticmethod
    def login():
        data = UserController.get_request_data()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        if not email or not password:
            return {
                'success': False,
                'user': None,
                'message': 'Email et password sont requis.'
            }, 400
        
        if not UserController.validate_email(email):
            return {
                'success': False,
                'message': 'Format d\'email invalide.'
            }, 400
    
        try:
            # Récupérer l'utilisateur de la BD
            user_data = Model.get('users', criteria={'email': email}, one=True)
            
            if user_data is None:
                return {
                    'success': False,
                    'message': 'Email ou mot de passe incorrect.'
                }, 401

            if not check_password_hash(user_data['password'], password):
                return {
                    'success': False,
                    'message': 'Email ou mot de passe incorrect.'
                }, 401
            
            user = User(user_data['id'], user_data['username'], user_data['email'])
            
            login_user(user)
            
            session.modified = True
            
            return {
                'success': True,
                'message': 'Connexion réussie !',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                },
            }, 200
            

        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la connexion: {str(e)}'
            }, 500
    
    @staticmethod
    def show_user(user_id):
        try:
            if not isinstance(user_id, int) or user_id <= 0:
                return {
                    'success': False,
                    'message': 'ID utilisateur invalide.'
                }, 400
            
            user = Model.get('users', criteria={'id': user_id}, one=True)
            
            if user is None:
                return {
                    'success': False,
                    'message': f'Utilisateur avec l\'ID {user_id} non trouvé.'
                }, 404
            
            return {
                'success': True,
                'user': user,
                'message': 'Utilisateur trouvé.'
            }, 200
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération de l\'utilisateur: {str(e)}'
            }, 500
    
    @staticmethod
    def show_all_users():
        try:
            users = Model.get('users', one=False)
            
            return {
                'success': True,
                'user': users,
                'message': f'{len(users)} utilisateur(s) trouvé(s).'
            }, 200
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération des utilisateurs: {str(e)}'
            }, 500
            
    @staticmethod
    def update_user(user_id):
        data = UserController.get_request_data()
        
        username = data.get('username', '').strip() if data.get('username') else None
        email = data.get('email', '').strip() if data.get('email') else None
        password = data.get('password', '').strip() if data.get('password') else None
        
        try:
            if not isinstance(user_id, int) or user_id <= 0:
                return {
                    'success': False,
                    'message': 'ID utilisateur invalide.'
                }, 400
            
            user = Model.get('users', criteria={'id': user_id}, one=True)
            
            if user is None:
                return {
                    'success': False,
                    'message': f'Utilisateur avec l\'ID {user_id} non trouvé.'
                }, 404
                
            data_to_update = {}

            if username is not None:
                if len(username) < 3:
                    return {
                        'success': False,
                        'message': 'Le username doit contenir au moins 3 caractères.'
                    }, 400
                data_to_update['username'] = username

            if email is not None:
                if not UserController.validate_email(email):
                    return {
                        'success': False,
                        'message': 'Format d\'email invalide.'
                    }, 400
                data_to_update['email'] = email
            
            if password is not None:
                is_valid, msg = UserController.validate_password(password)
                if not is_valid:
                    return {
                        'success': False,
                        'message': msg
                    }, 400
                data_to_update['password'] = generate_password_hash(password)

            if not data_to_update:
                return {
                    'success': False,
                    'message': 'Aucun champ à mettre à jour.'
                }, 400
            
            Model.update('users', user_id, data_to_update)
            
            return {
                'success': True,
                'message': 'Utilisateur mis à jour avec succès.'
            }, 200
        except sqlite3.IntegrityError:
            return {
                'success': False,
                'message': 'Ce nom d\'utilisateur ou email existe déjà.'
            }, 409
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la mise à jour: {str(e)}'
            }, 500
            
    @staticmethod
    def delete_user(user_id):
        try:
            if not isinstance(user_id, int) or user_id <= 0:
                return {
                    'success': False,
                    'message': 'ID utilisateur invalide.'
                }, 400
            
            user = Model.get('users', criteria={'id': user_id}, one=True)
            
            if user is None:
                return {
                    'success': False,
                    'message': f'Utilisateur avec l\'ID {user_id} non trouvé.'
                }, 404
            
            Model.delete('users', user_id)
            
            return {
                'success': True,
                'message': f'Utilisateur {user["username"]} supprimé avec succès.'
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la suppression: {str(e)}'
            }, 500
    
    @staticmethod
    def logout():
        logout_user()  # Utilise logout_user de Flask-Login
        return {
            'success': True,
            'message': 'Déconnexion réussie.'
        }, 200