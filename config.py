import os
from decouple import config
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = int( '587')
    MAIL_USE_TLS =  True
    MAIL_USERNAME = config('MAIL_USERNAME') 
    MAIL_PASSWORD = config('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = config('MAIL_USERNAME')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = config('SECRET_KEY') or 'hadrtoguessstring'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_POSTS_PER_PAGE = 3
    FLASKY_FOLLOWERS_PER_PAGE = 2
    FLASKY_COMMENTS_PER_PAGE = 3

    @staticmethod 
    def init_app(app): 
       pass

class DevelopmentConfig(Config): 
    DEBUG = True

    MAIL_SERVER = 'smtp.gmail.com' 
    MAIL_PORT = 465 
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = config('MAIL_USERNAME') 
    MAIL_PASSWORD = config('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config): 
    TESTING = True
    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = { 
   'development': DevelopmentConfig, 
   'testing': TestingConfig, 
    'production': ProductionConfig,
    'default': ProductionConfig
     } 