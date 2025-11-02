from flask import Flask, render_template, redirect, url_for, flash, jsonify, request
from flask_cors import CORS
import os
from Config.config import *
from Config.db import *
from Controllers.usersController import UserController, User
from Controllers.articlesController import PostController
from Controllers.commentsController import CommentsController

from flask_login import (
    LoginManager,
    login_required,
    current_user,
)
import logging

logger = LoggerSetup.setup_logging(app_name='api_server', log_dir='logs/api')


app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY', 'your_super_secret_key') 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ===== CONFIGURATION CORS =====
CORS(app, 
     origins=['http://localhost:3000'],  
     supports_credentials=True,
     allow_headers=['Content-Type', 'Authorization'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

app.config.from_object(__name__)

app.config.from_mapping(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=False  
)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

init_app(app)

# ===== USER LOADER =====
@login_manager.user_loader
def load_user(user_id):
    try:
        from Models.Model import Model
        user_data = Model.get('users', criteria={'id': int(user_id)}, one=True)
        if user_data:
            return User(user_data['id'], user_data['username'], user_data['email'])
    except Exception as e:
        logging.error(f"Erreur dans load_user: {str(e)}")
    return None

# ===== ROUTES =====

@app.route('/')
def index():
    return "My first page"

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    result, http_code = UserController.logout()    
    return jsonify(result), http_code
 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        result, http_code = UserController.register()
        
        if request.is_json:
            return jsonify(result), http_code

        if result['success']:
            flash(result['message'], 'success')
            return redirect(url_for('login'))
        else:
            flash(result['message'], 'danger')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        result, http_code = UserController.login()
        
        if request.is_json:
            return jsonify(result), http_code

        if result['success']:
            flash(result['message'], 'success')
            return redirect(url_for('index'))
        else:
            flash(result['message'], 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/users', methods=['GET'])
@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def users(user_id=None):
    if request.method == 'GET' and user_id is None:
        result, http_code = UserController.show_all_users()
        return jsonify(result), http_code

    if request.method == 'GET' and user_id is not None:
        result, http_code = UserController.show_user(user_id)
        return jsonify(result), http_code
    
    if request.method == 'PUT':
        if user_id is None:
            return jsonify({
                'success': False,
                'message': 'ID utilisateur requis pour la mise à jour.'
            }), 400
        
        result, http_code = UserController.update_user(user_id)
        return jsonify(result), http_code

    if request.method == 'DELETE':
        if user_id is None:
            return jsonify({
                'success': False,
                'message': 'ID utilisateur requis pour la suppression.'
            }), 400
        
        result, http_code = UserController.delete_user(user_id)
        return jsonify(result), http_code
    
@app.route('/posts', methods=['GET', 'POST'])
@app.route('/posts/<int:post_id>', methods=['GET', 'PUT', 'DELETE'])
def post(post_id=None):
    if post_id is None:
        if request.method == 'GET':
            result, http_code = PostController.show_all_posts()
            return jsonify(result), http_code
        
        elif request.method == 'POST':
            if not current_user.is_authenticated:
                return jsonify({
                    'success': False,
                    'message': 'Vous devez être connecté pour créer un post.'
                }), 401
            
            result, http_code = PostController.addPost()
            return jsonify(result), http_code
    else:
        if request.method == 'GET':
            result, http_code = PostController.show_post(post_id)
            return jsonify(result), http_code
        
        if request.method == 'PUT':
            if not current_user.is_authenticated:
                return jsonify({
                    'success': False,
                    'message': 'Vous devez être connecté pour modifier un post.'
                }), 401
            
            if post_id is None:
                return jsonify({
                    'success': False,
                    'message': 'ID du post requis pour la mise à jour.'
                }), 400
            
            result, http_code = PostController.update_post(post_id)
            return jsonify(result), http_code

        if request.method == 'DELETE':
            if not current_user.is_authenticated:
                return jsonify({
                    'success': False,
                    'message': 'Vous devez être connecté pour supprimer un post.'
                }), 401
            
            if post_id is None:
                return jsonify({
                    'success': False,
                    'message': 'ID post requis pour la suppression.'
                }), 400
            
            result, http_code = PostController.delete_post(post_id)
            return jsonify(result), http_code


@app.route('/my-posts', methods=['GET'])
@login_required
def my_posts():
    try:
        
        result, http_code = PostController.get_user_posts()
        
        return jsonify(result), http_code
    
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des posts: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Erreur: {str(e)}'
        }), 500


# ===== ROUTES COMMENTAIRES =====

"""Créer un commentaire"""
@app.route('/posts/<int:post_id>/comments', methods=['POST'])
@login_required
def create_comment(post_id):
    result, http_code = CommentsController.create_comment(post_id)
    return jsonify(result), http_code

"""Récupérer les commentaires d'un article"""
@app.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    result, http_code = CommentsController.get_article_comments(post_id)
    return jsonify(result), http_code

"""Récupérer un commentaire"""
@app.route('/comments/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    result, http_code = CommentsController.get_comment(comment_id)
    return jsonify(result), http_code

"""Mettre à jour un commentaire"""
@app.route('/comments/<int:comment_id>', methods=['PUT'])
@login_required
def update_comment(comment_id):
    result, http_code = CommentsController.update_comment(comment_id)
    return jsonify(result), http_code

"""Supprimer un commentaire"""
@app.route('/comments/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    result, http_code = CommentsController.delete_comment(comment_id)
    return jsonify(result), http_code

# ===== GESTIONNAIRE D'ERREURS =====
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'message': 'Non autorisé. Vous devez être connecté.'
    }), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'success': False,
        'message': 'Accès interdit.'
    }), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Ressource non trouvée.'
    }), 404

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)