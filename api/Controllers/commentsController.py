from flask import request, session
from flask_login import current_user, login_required
from Models.Model import Model
import logging
import sqlite3

class CommentsController:
    
    
    @staticmethod
    def validate_comment(message):
        if not message or len(message.strip()) < 1:
            return False, 'Le commentaire ne peut pas être vide.'
        if len(message) > 1000:
            return False, 'Le commentaire ne doit pas dépasser 1000 caractères.'
        return True, 'OK'
    
    
    @staticmethod
    def create_comment(post_id):
        
        
        if not current_user.is_authenticated:
            return {
                'success': False,
                'message': 'Vous devez être connecté pour commenter.'
            }, 401
        
        data = request.get_json()
        content = data.get('message', '').strip()
        user_id = current_user.id
        
        is_valid, msg = CommentsController.validate_comment(content)
        if not is_valid:
            return {
                'success': False,
                'message': msg
            }, 400
        
        try:
            article = Model.get('posts', criteria={'id': post_id}, one=True)
            if article is None:
                return {
                    'success': False,
                    'message': f'Article avec l\'ID {post_id} non trouvé.'
                }, 404
            
            comment_data = {
                'content': content,
                'post_id': post_id,
                'user_id': user_id
            }
            
            new_id = Model.create('comments', comment_data)
            
            return {
                'success': True,
                'message': 'Commentaire créé avec succès.',
                'comment_id': new_id
            }, 201
        
        except sqlite3.IntegrityError as e:
            return {
                'success': False,
                'message': f'Erreur de base de données: {str(e)}'
            }, 409
        
        except Exception as e:
            logging.error(f"Erreur création commentaire: {str(e)}")
            return {
                'success': False,
                'message': f'Erreur: {str(e)}'
            }, 500
    
    
    @staticmethod
    def get_article_comments(post_id):
        
        try:
            article = Model.get('posts', criteria={'id': post_id}, one=True)
            if article is None:
                return {
                    'success': False,
                    'message': f'Article avec l\'ID {post_id} non trouvé.'
                }, 404
            
            comments = Model.get('comments', criteria={'post_id': post_id}, one=False)
            
            if not comments:
                comments = []
            
            for comment in comments:
                user = Model.get('users', criteria={'id': comment['user_id']}, one=True)
                if user:
                    comment['username'] = user.get('username')
                    comment['email'] = user.get('email')
            
            return {
                'success': True,
                'comments': comments,
                'message': f'{len(comments)} commentaire(s) trouvé(s).'
            }, 200
        
        except Exception as e:
            logging.error(f"Erreur récupération commentaires: {str(e)}")
            return {
                'success': False,
                'message': f'Erreur: {str(e)}'
            }, 500
    @staticmethod
    def get_comment(comment_id):
        
        try:
            comment = Model.get('comments', criteria={'id': comment_id}, one=True)
            
            if comment is None:
                return {
                    'success': False,
                    'message': f'Commentaire avec l\'ID {comment_id} non trouvé.'
                }, 404
            
            return {
                'success': True,
                'comment': comment,
                'message': 'Commentaire trouvé.'
            }, 200
        
        except Exception as e:
            logging.error(f"Erreur récupération commentaire: {str(e)}")
            return {
                'success': False,
                'message': f'Erreur: {str(e)}'
            }, 500
    
    
    @staticmethod
    def update_comment(comment_id):
        
        if not current_user.is_authenticated:
            return {
                'success': False,
                'message': 'Vous devez être connecté pour modifier un commentaire.'
            }, 401
        
        data = request.get_json()
        content = data.get('message', '').strip()
        
        is_valid, msg = CommentsController.validate_comment(content)
        if not is_valid:
            return {
                'success': False,
                'message': msg
            }, 400
        
        try:
            comment = Model.get('comments', criteria={'id': comment_id}, one=True)
            
            if comment is None:
                return {
                    'success': False,
                    'message': f'Commentaire avec l\'ID {comment_id} non trouvé.'
                }, 404
            
            if comment['user_id'] != current_user.id:
                return {
                    'success': False,
                    'message': 'Vous n\'êtes pas autorisé à modifier ce commentaire.'
                }, 403
            
            update_data = {'content': content}
            Model.update('comments', comment_id, update_data)
            
            return {
                'success': True,
                'message': 'Commentaire mis à jour avec succès.'
            }, 200
        
        except sqlite3.IntegrityError as e:
            return {
                'success': False,
                'message': f'Erreur de base de données: {str(e)}'
            }, 409
        
        except Exception as e:
            logging.error(f"Erreur mise à jour commentaire: {str(e)}")
            return {
                'success': False,
                'message': f'Erreur: {str(e)}'
            }, 500
    
    
    @staticmethod
    def delete_comment(comment_id):
        
        if not current_user.is_authenticated:
            return {
                'success': False,
                'message': 'Vous devez être connecté pour supprimer un commentaire.'
            }, 401
        
        try:
            comment = Model.get('comments', criteria={'id': comment_id}, one=True)
            
            if comment is None:
                return {
                    'success': False,
                    'message': f'Commentaire avec l\'ID {comment_id} non trouvé.'
                }, 404
            
            if comment['user_id'] != current_user.id:
                return {
                    'success': False,
                    'message': 'Vous n\'êtes pas autorisé à supprimer ce commentaire.'
                }, 403
            
            Model.delete('comments', comment_id)
            
            return {
                'success': True,
                'message': 'Commentaire supprimé avec succès.'
            }, 200
        
        except Exception as e:
            logging.error(f"Erreur suppression commentaire: {str(e)}")
            return {
                'success': False,
                'message': f'Erreur: {str(e)}'
            }, 500