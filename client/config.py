import os

#  API SERVER 
API_SERVER = os.getenv('API_SERVER', 'http://localhost:5000')
API_TIMEOUT = int(os.getenv('API_TIMEOUT', 30))

#  FLASK CONFIG 
DEBUG = os.getenv('DEBUG', True)
SECRET_KEY = os.getenv('SECRET_KEY', 'client_secret_key_12345')
TESTING = os.getenv('TESTING', False)

#  SERVER CONFIG 
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 3000))
THREADED = True

#  SESSION 
PERMANENT_SESSION_LIFETIME = 3600  # 1 heure
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# LOGGING
LOG_FILE = 'client.log'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')

# FEATURES
ENABLE_COMMENTS = True
ENABLE_LIKES = False
ENABLE_NOTIFICATIONS = False

# VALIDATION

# Username
USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 50

# Email
EMAIL_MAX_LENGTH = 120

# Password
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 120

# Article
ARTICLE_TITLE_MIN_LENGTH = 3
ARTICLE_TITLE_MAX_LENGTH = 200
ARTICLE_BODY_MIN_LENGTH = 10
ARTICLE_BODY_MAX_LENGTH = 10000

# Comment
COMMENT_MIN_LENGTH = 1
COMMENT_MAX_LENGTH = 1000

ITEMS_PER_PAGE = 10

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
IS_PRODUCTION = ENVIRONMENT == 'production'
IS_DEVELOPMENT = ENVIRONMENT == 'development'

print(f"""
╔═══════════════════════════════════════╗
║   CLIENT CONFIGURATION LOADED          ║
╠═══════════════════════════════════════╣
║ Environment: {ENVIRONMENT:<25} ║
║ API Server: {API_SERVER:<24} ║
║ Debug: {str(DEBUG):<31} ║
║ Port: {PORT:<32} ║
╚═══════════════════════════════════════╝
""")