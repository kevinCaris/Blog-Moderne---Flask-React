"""
Client Flask App - Routes Flask
"""

from flask import Flask, render_template, redirect, url_for, jsonify, request
import os
import logging
from Controllers.UsersController import UsersController
from Controllers.ArticlesController import ArticlesController
from Controllers.CommentsController import CommentsController

from config import *

logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__, 
            template_folder='Templates',
            static_folder='static',
            static_url_path='/static')

app.secret_key = os.getenv('SECRET_KEY', 'client_secret_key_12345')


# ***** ROUTES: HOME *****

"""Page d'accueil"""
@app.route('/')
def index():
    _, articles, _= ArticlesController.get_all_articles()

    return ArticlesController.show_articles_page(articles)


# ***** ROUTES: AUTHENTIFICATION *****

"""Page d'inscription"""
@app.route('/register', methods=['GET', 'POST'])
def register():
    
    if request.method == 'GET':
        return UsersController.show_register_page()
    
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    password_confirm = request.form.get('passwordConfirm', '')
    
    is_valid, errors = UsersController.validate_register_form(
        username, email, password, password_confirm
    )
    
    if not is_valid:
        return render_template('register.html', errors=errors), 400
    
    success, api_data, status_code = UsersController.register_user(
        username, email, password
    )
    
    if success:
        return render_template('login.html', 
                             message=api_data.get('message')), 201
    else:
        errors = [api_data.get('message', 'Une erreur est survenue')]
        return render_template('register.html', errors=errors), status_code
    

"""Page de connexion"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'GET':
        return UsersController.show_login_page()
    
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    
    is_valid, errors = UsersController.validate_login_form(email, password)
    
    if not is_valid:
        return render_template('login.html', errors=errors), 400
    
    # Appel API
    success, api_data, status_code = UsersController.login_user(email, password)
    
    if success:
        user = api_data.get('user')
        
        UsersController.set_user_session(
            user.get('id'),
            user.get('username'),
            user.get('email')
        )
        
        return redirect(url_for('index'))
    else:
        errors = [api_data.get('message', 'Email ou mot de passe incorrect')]
        return render_template('login.html', errors=errors), status_code
    

"""Déconnexion"""
@app.route('/logout')
def logout():
    
    UsersController.logout_user()
    UsersController.clear_user_session()
    
    return redirect(url_for('index'))


# ***** ROUTES: PROFIL *****

@app.route('/profile')
@UsersController.require_login
def profile():
    """Page profil utilisateur (protégée)"""
    user = UsersController.get_logged_user()
    return render_template('profile.html', user=user)


# ***** ROUTES: ARTICLES *****

"""Articles de l'utilisateur connecté"""
@app.route('/articles')
@UsersController.require_login
def user_articles():
    user = UsersController.get_logged_user()
    
    success, articles, status_code = ArticlesController.get_all_articles()
    print(articles)
    if success:
        user_articles_list = [a for a in articles if a.get('user_id') == user.get('id')]
        return render_template('my_articles.html', 
                             user=user, 
                             articles=user_articles_list)
    else:
        return render_template('my_articles.html', 
                             user=user, 
                             articles=[],
                             error=articles), 400

@app.route('/articles/create', methods=['GET', 'POST'])
@UsersController.require_login
def create_article():
    """Créer un nouvel article"""
    
    if request.method == 'GET':
        return render_template('create_article.html')
    
    title = request.form.get('title', '').strip()
    body = request.form.get('body', '').strip()
    
    is_valid, errors = ArticlesController.validate_article_form(title, body)
    
    if not is_valid:
        return render_template('create_article.html', errors=errors), 400
    
    success, api_data, status_code = ArticlesController.create_article(title, body)
    
    if success:
        return redirect(url_for('user_articles'))
    else:
        errors = [api_data.get('message', 'Erreur inconnue')]
        return render_template('create_article.html', errors=errors), status_code
    

"""Détail d'un article"""
@app.route('/articles/<int:article_id>')
def article_detail(article_id):
    return ArticlesController.show_article_detail(article_id)

"""Éditer un article (protégé)"""
@app.route('/articles/<int:article_id>/edit', methods=['GET', 'POST'])
@UsersController.require_login
def edit_article(article_id):
    
    user = UsersController.get_logged_user()
    
    if request.method == 'GET':
        success, article, status_code = ArticlesController.get_article(article_id)
        
        if not success:
            return redirect(url_for('index'))
        
        if article.get('user_id') != user.get('id'):
            return redirect(url_for('article_detail', article_id=article_id)), 403
        
        return render_template('edit_article.html', article=article)
    
    title = request.form.get('title', '').strip()
    body = request.form.get('body', '').strip()
    
    is_valid, errors = ArticlesController.validate_article_form(title, body)
    
    if not is_valid:
        return render_template('edit_article.html', errors=errors), 400
    
    success, api_data, status_code = ArticlesController.update_article(article_id, title, body)
    
    if success:
        return redirect(url_for('article_detail', article_id=article_id))
    else:
        errors = [api_data.get('message', 'Erreur inconnue')]
        return render_template('edit_article.html', errors=errors), status_code
    
"""Supprimer un article """
@app.route('/articles/<int:article_id>/delete', methods=['POST'])
@UsersController.require_login
def delete_article(article_id):
    
    user = UsersController.get_logged_user()
    
    success_get, article, _ = ArticlesController.get_article(article_id)
    
    if not success_get or article.get('user_id') != user.get('id'):
        return redirect(url_for('article_detail', article_id=article_id)), 403
    
    success, api_data, status_code = ArticlesController.delete_article(article_id)
    
    if success:
        return redirect(url_for('user_articles'))
    else:
        return redirect(url_for('article_detail', article_id=article_id)), status_code

# ***** API ROUTES *****


"""Récupérer tous les articles"""
@app.route('/api/posts', methods=['GET'])
def api_get_posts():
    success, articles, status_code = ArticlesController.get_all_articles()
    
    return jsonify({
        'success': success,
        'post': articles
    }), status_code
    
    
"""Récupérer un article"""
@app.route('/api/posts/<int:post_id>', methods=['GET'])
def api_get_post(post_id):
    success, article, status_code = ArticlesController.get_article(post_id)
    
    return jsonify({
        'success': success,
        'post': article
    }), status_code


""" Mettre à jour un article"""
@app.route('/api/posts/<int:post_id>', methods=['PUT'])
@UsersController.require_login
def api_update_post(post_id):
    
    request_data = request.get_json()
    title = request_data.get('title', '').strip()
    body = request_data.get('body', '').strip()
    
    is_valid, errors = ArticlesController.validate_article_form(title, body)
    
    if not is_valid:
        return jsonify({
            'success': False,
            'errors': errors
        }), 400
    
    success, data, status_code = ArticlesController.update_article(post_id, title, body)
    
    return jsonify({
        'success': success,
        'message': data.get('message', '')
    }), status_code


"""Supprimer un article"""
@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
@UsersController.require_login
def api_delete_post(post_id):
    
    success, data, status_code = ArticlesController.delete_article(post_id)
    
    return jsonify({
        'success': success,
        'message': data.get('message', '')
    }), status_code


# ===== ROUTES COMMENTAIRES =====

"""Récupérer les commentaires d'un article"""
@app.route('/api/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    success, comments, status_code = CommentsController.get_article_comments(post_id)
    return jsonify({
        'success': success,
        'comments': comments
    }), status_code


"""Créer un commentaire"""
@app.route('/api/comments', methods=['POST'])
@UsersController.require_login
def create_comment():
    article_id = request.json.get('article_id')
    message = request.json.get('message')
    
    success, data, status_code = CommentsController.create_comment(article_id, message)
    return jsonify(data), status_code


"""Mettre à jour un commentaire"""
@app.route('/api/comments/<int:comment_id>', methods=['PUT'])
@UsersController.require_login
def update_comment(comment_id):
    message = request.json.get('message')
    
    success, data, status_code = CommentsController.update_comment(comment_id, message)
    return jsonify(data), status_code


@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
@UsersController.require_login
def delete_comment(comment_id):
    """Supprimer un commentaire"""
    success, data, status_code = CommentsController.delete_comment(comment_id)
    return jsonify(data), status_code

# ***** ERROR HANDLERS *****

@app.errorhandler(401)
def unauthorized(e):
    return redirect(url_for('login')), 401

@app.errorhandler(403)
def forbidden(e):
    return redirect(url_for('index')), 403

@app.errorhandler(404)
def not_found(e):
    return redirect(url_for('index')), 404

@app.errorhandler(500)
def server_error(e):
    return redirect(url_for('index')), 500

# ***** CONTEXT PROCESSORS *****

@app.context_processor
def inject_user():
    user = UsersController.get_logged_user() if UsersController.is_user_login() else None
    return {'current_user': user}

@app.context_processor
def inject_is_logged_in():
    return {'is_logged_in': UsersController.is_user_login()}


if __name__ == '__main__':
    
    app.run(host=HOST, port=PORT, debug=DEBUG, threaded=THREADED)