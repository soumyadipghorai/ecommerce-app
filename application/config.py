import os 
basedir = os.path.abspath(os.path.dirname(__file__))

class Config() : 
    DEBUG = False 
    SQLITE_DB_DIR = None 
    SQLALCHEMY_DATABASE_URI = None 
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    WTF_CSRF_ENABLED = False 
    SECURITY_TOKEN_AUTHENCTICATION_HEADER = "Authentication-Token"

    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = "redis://localhost:6379"
    CELERY_WORKER_CONCURRENCY = 1000

    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379

class LocalDevelopmentConfig(Config) : 
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(SQLITE_DB_DIR, 'ecomdb.sqlite3')
    DEBUG = True 
    SECRET_KEY = "CJN178&^w%@&%w&@!wcwd19(*!#812C39EJNF"
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = "!(*@jqschdUH17121iqhdd9wduqwd)"
    SECURITY_REGISTERABLE = True 
    SECURITY_SEND_REGISTER_EMAIL = False 
    SECURITY_UNAUTHORIZED_VIEW = None
    CELERY_BROKER_URL = 'redis://localhost:6379'
    CELERY_RESULT_BACKEND = "redis://localhost:6379" 
    WTF_CSRF_ENABLED = False 

    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
"""
class ProductionDevelopmentConfig(Config) : 
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(SQLITE_DB_DIR, 'proddb.sqlite3')
    DEBUG = False 
    PASSWORD = os.getenv('PASSWORD')
"""