from datetime import timedelta
from F_taste_dieta.utils.credentials import secret_key
import os
basedir = os.path.abspath(os.path.dirname(__file__))
from F_taste_dieta.utils.config_loader import config_data


class Config(object):
    TESTING = False
''' config vecchia che prende da file env
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI','postgresql://postgres:Bcsoftqwerty@localhost:5432/f-taste')
    DB_URI_PATIENT = os.environ.get('DB_URI_PATIENT', 'postgresql://patient:patient@localhost:5432/f-taste')
    DB_URI_ADMIN = os.environ.get('DB_URI_ADMIN', 'postgresql://f_taste_admin:admin@localhost:5432/f-taste')
    DB_URI_DIETITIAN = os.environ.get('DB_URI_DIETITIAN', 'postgresql://dietitian:dietitian@localhost:5432/f-taste')
    RAISE_EXCEPTIONS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = secret_key
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    ERROR_INCLUDE_MESSAGE  = True
    RESTX_VALIDATE = True
    RATELIMIT_ENABLED = False
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)
'''
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = config_data.get("SQLALCHEMY_DATABASE_URI", "sqlite:///default.db")
    DB_URI_PATIENT = config_data.get("DB_URI_PATIENT", "sqlite:///default.db")
    DB_URI_ADMIN = config_data.get("DB_URI_ADMIN", "sqlite:///default.db")
    DB_URI_DIETITIAN = config_data.get("DB_URI_DIETITIAN", "sqlite:///default.db")
    
    JWT_SECRET_KEY = bytes.fromhex(config_data.get("JWT_SECRET_KEY", "f20adf0723d64a2f2088a0b4270fc715"))
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=config_data.get("JWT_ACCESS_TOKEN_EXPIRES", 3600))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=config_data.get("JWT_REFRESH_TOKEN_EXPIRES", 2592000))

    REDIS_HOST = config_data.get("REDIS_HOST", "localhost")
    REDIS_PORT = config_data.get("REDIS_PORT", 6379)
    REDIS_PASSWORD = config_data.get("REDIS_PASSWORD", None)


config = {
    'dev': DevelopmentConfig
}