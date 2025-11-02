"""
Articles Controller
validation + appels API pour les articles
"""
import requests
from config import API_SERVER, API_TIMEOUT
from flask import render_template, redirect, url_for, session


class ArticlesController:
    
    # ===== VALIDATION =====
    
    @staticmethod
    def validate_article_title(title):
        if not title or len(title.strip()) < 3:
            return False, 'Le titre doit contenir au moins 3 caractères.'
        if len(title) > 200:
            return False, 'Le titre ne doit pas dépasser 200 caractères.'
        return True, 'OK'
    
    
    @staticmethod
    def validate_article_body(body):
        if not body or len(body.strip()) < 10:
            return False, 'Le contenu doit contenir au moins 10 caractères.'
        if len(body) > 10000:
            return False, 'Le contenu ne doit pas dépasser 10000 caractères.'
        return True, 'OK'
    
    
    @staticmethod
    def validate_article_form(title, body):
        errors = []
        
        is_valid, msg = ArticlesController.validate_article_title(title)
        if not is_valid:
            errors.append(msg)
        
        is_valid, msg = ArticlesController.validate_article_body(body)
        if not is_valid:
            errors.append(msg)
        
        return len(errors) == 0, errors
    
    
    @staticmethod
    def validate_comment(message):
        if not message or len(message.strip()) < 1:
            return False, 'Le commentaire ne peut pas être vide.'
        if len(message) > 1000:
            return False, 'Le commentaire ne doit pas dépasser 1000 caractères.'
        return True, 'OK'
    
    
    # ===== APPELS API =====
    
    @staticmethod
    def _get_cookies():
        return session.get('cookies', {})
    
    @staticmethod
    def create_article(title, body):
        
        try:
            response = requests.post(
                f'{API_SERVER}/posts',
                json={
                    'title': title,
                    'body': body
                },
                timeout=API_TIMEOUT,
                cookies=ArticlesController._get_cookies()
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
    def get_all_articles():
        
        try:
            response = requests.get(
                f'{API_SERVER}/posts',
                timeout=API_TIMEOUT,
                cookies=ArticlesController._get_cookies()
            )
            
            data = response.json()
            
            articles = data.get('post', [])  
            return data.get('success', True), articles, response.status_code
        
        except requests.exceptions.Timeout:
            return False, [], 504
        
        except requests.exceptions.ConnectionError:
            return False, [], 503
        
        except Exception as e:
            return False, [], 500
    
    @staticmethod
    def get_article(article_id):
        
        try:
            response = requests.get(
                f'{API_SERVER}/posts/{article_id}',
                timeout=API_TIMEOUT,
                cookies=ArticlesController._get_cookies()
            )
            
            data = response.json()
            
            article = data.get('post')
            return data.get('success', False), article, response.status_code
        
        except requests.exceptions.Timeout:
            return False, None, 504
        
        except requests.exceptions.ConnectionError:
            return False, None, 503
        
        except Exception as e:
            return False, None, 500
    
    @staticmethod
    def get_my_articles():
          
        try:
            response = requests.get(
                f'{API_SERVER}/my-posts',
                timeout=API_TIMEOUT,
                cookies=ArticlesController._get_cookies()
            )
            
            data = response.json()
            print(f'data {data}')
            
            articles = data.get('posts', [])
            return data.get('success', True), articles, response.status_code
        
        except requests.exceptions.Timeout:
            return False, [], 504
        
        except requests.exceptions.ConnectionError:
            return False, [], 503
        
        except Exception as e:
            return False, [], 500
        
    @staticmethod
    def update_article(article_id, title, body):
        
        try:
            response = requests.put(
                f'{API_SERVER}/posts/{article_id}',
                json={
                    'title': title,
                    'body': body
                },
                timeout=API_TIMEOUT,
                cookies=ArticlesController._get_cookies()
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
    def delete_article(article_id):
        
        try:
            response = requests.delete(
                f'{API_SERVER}/posts/{article_id}',
                timeout=API_TIMEOUT,
                cookies=ArticlesController._get_cookies()
            )
            
            data = response.json()
            
            return data.get('success', False), data, response.status_code
        
        except requests.exceptions.Timeout:
            return False, {'message': 'Timeout: L\'API ne répond pas'}, 504
        
        except requests.exceptions.ConnectionError:
            return False, {'message': 'Erreur: Impossible de se connecter à l\'API'}, 503
        
        except Exception as e:
            return False, {'message': f'Erreur: {str(e)}'}, 500
    
    # ===== COMMENTAIRES =====
    
    @staticmethod
    def create_comment(article_id, message):
        
        try:
            response = requests.post(
                f'{API_SERVER}/posts/{article_id}/comments',
                json={'message': message},
                timeout=API_TIMEOUT,
                cookies=ArticlesController._get_cookies()
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
                cookies=ArticlesController._get_cookies()
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
    
    # ===== TEMPLATES =====
    
    @staticmethod
    def show_articles_page(data):
        return render_template('index.html',posts=data)
    
    @staticmethod
    def show_article_detail(article_id):
        success, article, status_code = ArticlesController.get_article(article_id)
        
        if not success:
            return redirect(url_for('index'))
        
        return render_template('article_detail.html', article=article, comments=None)
    
    # ===== HELPERS =====
    
    @staticmethod
    def sanitize_article(article):
        if not article:
            return None
        
        return {
            'id': article.get('id'),
            'title': article.get('title', '').strip(),
            'body': article.get('body', '').strip(),
            'user_id': article.get('user_id'),
            'creationDate': article.get('creationDate')
        }

    
    @staticmethod
    def prepare_articles_for_display(articles):
        if not articles:
            return []
        
        return [ArticlesController.sanitize_article(article) for article in articles]