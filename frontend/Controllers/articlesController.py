from flask import request, session
from flask_login import current_user, login_required
from Models.Model import Model
import logging
import sqlite3

class PostController:
    
    @staticmethod
    def get_request_data():
        if request.is_json:
            return request.get_json()
        else:
            return request.form.to_dict()
        
    @staticmethod
    def addPost():
        # Vérifier que l'utilisateur est authentifié
        if not current_user.is_authenticated:
            return {
                'success': False,
                'message': 'Vous devez être connecté pour créer un post.'
            }, 401
        
        data = PostController.get_request_data()
        
        title = data.get('title', '').strip()
        body = data.get('body', '').strip()
        user_id = current_user.id  # Récupérer l'ID de l'utilisateur authentifié
        
        if not title or not body:
            return {
                'success': False,
                'message': 'title et body sont requis.'
            }, 400
        
        try:
            post_data = {
                "title": title,
                "body": body,
                "user_id": user_id 
            }

            new_id = Model.create('posts', post_data)
        
            return {
                'success': True,
                'message': 'Post créé avec succès.',
                'post_id': new_id 
            }, 201
        except sqlite3.IntegrityError as e:
            return {
                'success': False,
                'message': f'Erreur de contrainte de base de données: {str(e)}'
            }, 409
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de l\'ajout du post: {str(e)}'
            }, 500

    @staticmethod
    def show_post(post_id):
        try:
            post = Model.get('posts', criteria={'id': post_id}, one=True)
            
            if post is None:
                return {
                    'success': False,
                    'message': f'Post avec l\'ID {post_id} non trouvé.'
                }, 404
              
            return {
                'success': True,
                'post': post,
                'message': 'Post trouvé.'
            }, 200
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération du post: {str(e)}'
            }, 500
    
    @staticmethod
    def show_all_posts():
        try:
            posts = Model.get('posts', one=False)
            
            return {
                'success': True,
                'post': posts,
                'message': f'{len(posts)} Post(s) trouvé(s).'
            }, 200
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération des posts: {str(e)}'
            }, 500
            
    @staticmethod
    def update_post(post_id):
        # Vérifier que l'utilisateur est authentifié
        if not current_user.is_authenticated:
            return {
                'success': False,
                'message': 'Vous devez être connecté pour modifier un post.'
            }, 401
        
        data = PostController.get_request_data()
        user_id = current_user.id
        
        try:
            existing_post = Model.get('posts', criteria={'id': post_id}, one=True)
            
            if existing_post is None:
                return {
                    'success': False,
                    'message': f'Post avec l\'ID {post_id} non trouvé.'
                }, 404
                
            # Vérifier que l'utilisateur est propriétaire du post
            if existing_post['user_id'] != user_id:
                return {
                     'success': False,
                     'message': 'Vous n\'êtes pas autorisé à modifier ce post.'
                }, 403 
            
            update_data = {
                key: value 
                for key, value in data.items()
                if value is not None and key in ['title', 'body']
            }
            
            if not update_data:
                return {
                    'success': False,
                    'message': 'Aucun champ à mettre à jour.'
                }, 400
            
            Model.update('posts', post_id, update_data)
            
            return {
                'success': True,
                'message': f'Post avec l\'ID {post_id} mis à jour avec succès.'
            }, 200
            
        except sqlite3.IntegrityError as e:
            return {
                'success': False,
                'message': f'Erreur de contrainte de base de données: {str(e)}'
            }, 409
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la mise à jour: {str(e)}'
            }, 500
    
    @staticmethod
    def delete_post(post_id):
        # Vérifier que l'utilisateur est authentifié
        if not current_user.is_authenticated:
            return {
                'success': False,
                'message': 'Vous devez être connecté pour supprimer un post.'
            }, 401
            
        user_id = current_user.id

        try:
            post = Model.get('posts', criteria={'id': post_id}, one=True)
            
            if post is None:
                return {
                    'success': False,
                    'message': f'Post avec l\'ID {post_id} non trouvé.'
                }, 404
                
            # Vérifier que l'utilisateur est propriétaire du post
            if post['user_id'] != user_id:
                return {
                    'success': False,
                    'message': 'Vous n\'êtes pas autorisé à supprimer ce post.'
                }, 403
            
            Model.delete('posts', post_id)
            
            return {
                'success': True,
                'message': f'Post {post["title"]} supprimé avec succès.'
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la suppression: {str(e)}'
            }, 500  
            
    @staticmethod
    def get_user_posts():
        
        user_id=current_user.id
        try:
            user = Model.get('users', criteria={'id': user_id}, one=True)
            if user is None:
                return {
                    'success': False,
                    'message': f'Utilisateur avec l\'ID {user_id} non trouvé.'
                }, 404
            
            posts = Model.get('posts', criteria={'user_id': user_id}, one=False)
            
            if not posts:
                posts = []
            
            return {
                'success': True,
                'posts': posts,
                'user_id': user_id,
                'username': user.get('username'),
                'message': f'{len(posts)} post(s) trouvé(s).'
            }, 200
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération des posts: {str(e)}'
            }, 500