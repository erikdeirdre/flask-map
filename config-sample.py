import os


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY') or 'google api key'
    APP_NAME = os.environ.get('APP_NAME') or 'town-mapper'
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or '/tmp'
    ALLOWED_EXTENSIONS = os.environ.get('ALLOWED_EXTENSIONS') or \
                         {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    basedir = os.path.abspath(os.path.dirname(__file__))
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    pass
