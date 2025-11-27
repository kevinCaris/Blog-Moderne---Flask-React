"""
Users Controller
validation + appels API
"""
from flask import render_template, url_for, redirect, session
from functools import wraps
import re
import requests
from config import API_SERVER, API_TIMEOUT

class UsersController:
    
    # ===== VALIDATION =====
    
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
    def validate_username(username):
        if not username or len(username) < 3:
            return False, 'Le username doit contenir au moins 3 caractères.'
        if len(username) > 50:
            return False, 'Le username ne doit pas dépasser 50 caractères.'
        return True, 'OK'
    
    @staticmethod
    def validate_register_form(username, email, password, password_confirm):
        errors = []
        
        is_valid, msg = UsersController.validate_username(username)
        if not is_valid:
            errors.append(msg)
        
        if not email:
            errors.append('Email est requis.')
        elif not UsersController.validate_email(email):
            errors.append('Format d\'email invalide.')
        
        if not password:
            errors.append('Mot de passe est requis.')
        else:
            is_valid, msg = UsersController.validate_password(password)
            if not is_valid:
                errors.append(msg)
        
        if password != password_confirm:
            errors.append('Les mots de passe ne correspondent pas.')
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_login_form(email, password):
        errors = []
        
        if not email:
            errors.append('Email est requis.')
        elif not UsersController.validate_email(email):
            errors.append('Format d\'email invalide.')
        
        if not password:
            errors.append('Mot de passe est requis.')
        
        return len(errors) == 0, errors
    
    # ===== APPELS API =====
    
    @staticmethod
    def register_user(username, email, password):
        
        try:
            response = requests.post(
                f'{API_SERVER}/register',
                json={
                    'username': username,
                    'email': email,
                    'password': password
                },
                timeout=API_TIMEOUT
            )
            
            data = response.json()
            
            return data.get('success', False), data, response.status_code
        
        except requests.exceptions.Timeout:
            return False, {'message': 'Timeout: L\'API ne répond pas'}, 504
        
        except requests.exceptions.ConnectionError:
            return False, {'message': 'Erreur: Impossible de se connecter à l\'API'}, 503
        
        except Exception as e:
            return False, {'message': f'Erreur: {str(e)}'}, 500
    
    @staticmethod
    def login_user(email, password):
        
        try:
            response = requests.post(
                f'{API_SERVER}/login',
                json={
                    'email': email,
                    'password': password
                },
                timeout=API_TIMEOUT
            )
            
            data = response.json()
            
            if response.status_code == 200 and data.get('success'):
                cookies_dict = requests.utils.dict_from_cookiejar(response.cookies)
                session['cookies'] = cookies_dict
            
            return data.get('success', False), data, response.status_code
        
        except requests.exceptions.Timeout:
            return False, {'message': 'Timeout: L\'API ne répond pas'}, 504
        
        except requests.exceptions.ConnectionError:
            return False, {'message': 'Erreur: Impossible de se connecter à l\'API'}, 503
        
        except Exception as e:
            return False, {'message': f'Erreur: {str(e)}'}, 500
    
    @staticmethod
    def logout_user():
        
        try:
            # Envoyer les cookies avec la requête de logout
            cookies = session.get('cookies', {})
            requests.get(
                f'{API_SERVER}/logout',
                timeout=API_TIMEOUT,
                cookies=cookies
            )
        except Exception as e:
            pass  
    
    @staticmethod
    def make_authenticated_request(method, endpoint, data=None):
        
        cookies = session.get('cookies', {})
        url = f'{API_SERVER}{endpoint}'
        
        try:
            if method == 'GET':
                response = requests.get(url, timeout=API_TIMEOUT, cookies=cookies)
            elif method == 'POST':
                response = requests.post(url, json=data, timeout=API_TIMEOUT, cookies=cookies)
            elif method == 'PUT':
                response = requests.put(url, json=data, timeout=API_TIMEOUT, cookies=cookies)
            elif method == 'DELETE':
                response = requests.delete(url, timeout=API_TIMEOUT, cookies=cookies)
            else:
                return False, {'message': 'Méthode HTTP invalide'}, 400
            
            data = response.json()
            return data.get('success', False), data, response.status_code
        
        except requests.exceptions.Timeout:
            return False, {'message': 'Timeout: L\'API ne répond pas'}, 504
        except requests.exceptions.ConnectionError:
            return False, {'message': 'Erreur: Impossible de se connecter à l\'API'}, 503
        except Exception as e:
            return False, {'message': f'Erreur: {str(e)}'}, 500
    
    # ===== SESSION =====
    
    @staticmethod
    def is_user_login():
        return 'user_id' in session
    
    @staticmethod
    def get_logged_user():
        if UsersController.is_user_login():
            return {
                'id': session.get('user_id'),
                'username': session.get('username'),
                'email': session.get('email')
            }
        return None
    
    @staticmethod
    def set_user_session(user_id, username, email):
        session['user_id'] = user_id
        session['username'] = username
        session['email'] = email
    
    @staticmethod
    def clear_user_session():
        session.pop('user_id', None)
        session.pop('username', None)
        session.pop('email', None)
        session.pop('cookies', None)  
    
    # ===== TEMPLATES =====
    
    @staticmethod
    def show_register_page():
        return render_template('register.html')
    
    @staticmethod
    def show_login_page():
        return render_template('login.html')
    
    # ===== DÉCORATEUR =====
    
    @staticmethod
    def require_login(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not UsersController.is_user_login():
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        
        return decorated_function
    
    