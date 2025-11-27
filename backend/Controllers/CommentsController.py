import requests
from config import API_SERVER, API_TIMEOUT
from flask import session


class CommentsController:
    
    
    @staticmethod
    def validate_comment(message):
        if not message or len(message.strip()) < 1:
            return False, 'Le commentaire ne peut pas être vide.'
        if len(message) > 1000:
            return False, 'Le commentaire ne doit pas dépasser 1000 caractères.'
        return True, 'OK'
    
    
    @staticmethod
    def _get_cookies():
        return session.get('cookies', {})
    
    
    @staticmethod
    def create_comment(article_id, message):
        
        
        is_valid, msg = CommentsController.validate_comment(message)
        if not is_valid:
            return False, {'message': msg}, 400
        
        try:
            response = requests.post(
                f'{API_SERVER}/posts/{article_id}/comments',
                json={'message': message},
                timeout=API_TIMEOUT,
                cookies=CommentsController._get_cookies()
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
    def get_article_comments(article_id):
                
        try:
            response = requests.get(
                f'{API_SERVER}/posts/{article_id}/comments',
                timeout=API_TIMEOUT,
                cookies=CommentsController._get_cookies()
            )
            
            data = response.json()
            
            comments = data.get('comments', [])
            return data.get('success', False), comments, response.status_code
        
        except requests.exceptions.Timeout:
            return False, [], 504
        
        except requests.exceptions.ConnectionError:
            return False, [], 503
        
        except Exception as e:
            return False, [], 500
    
    @staticmethod
    def get_comment(comment_id):
                
        try:
            response = requests.get(
                f'{API_SERVER}/comments/{comment_id}',
                timeout=API_TIMEOUT,
                cookies=CommentsController._get_cookies()
            )
            
            data = response.json()
            
            comment = data.get('comment')
            return data.get('success', False), comment, response.status_code
        
        except requests.exceptions.Timeout:
            return False, None, 504
        
        except requests.exceptions.ConnectionError:
            return False, None, 503
        
        except Exception as e:
            return False, None, 500
    
    
    @staticmethod
    def update_comment(comment_id, message):
        
        
        is_valid, msg = CommentsController.validate_comment(message)
        if not is_valid:
            return False, {'message': msg}, 400
        
        try:
            response = requests.put(
                f'{API_SERVER}/comments/{comment_id}',
                json={'message': message},
                timeout=API_TIMEOUT,
                cookies=CommentsController._get_cookies()
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
    def delete_comment(comment_id):
                
        try:
            response = requests.delete(
                f'{API_SERVER}/comments/{comment_id}',
                timeout=API_TIMEOUT,
                cookies=CommentsController._get_cookies()
            )
            
            data = response.json()
            
            return data.get('success', False), data, response.status_code
        
        except requests.exceptions.Timeout:
            return False, {'message': 'Timeout: L\'API ne répond pas'}, 504
        
        except requests.exceptions.ConnectionError:
            return False, {'message': 'Erreur: Impossible de se connecter à l\'API'}, 503
        
        except Exception as e:
            return False, {'message': f'Erreur: {str(e)}'}, 500