'''
项目配置类
'''

import os
import sys

basedir=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
WIN=sys.platform.startswith('win')
if WIN:
    prefix='sqlite:///'
else:
    prefix='sqlite:////'

class BaseConfig:
    ITEM_PER_PAGE=20

    SECRET_KEY=os.getenv('SECRET_KEY','secret key')

    SQLALCHEMY_TRACK_MODIFICATIONS=False

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI=prefix+os.path.join(basedir,'data-dev.db')

class TestingConfig(BaseConfig):
    TESTING=True
    WTF_CSRF_ENABLED=False
    SQLALCHEMY_DATABASE_URI=prefix+':memory:'

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL',prefix+os.path.join(basedir,'data.db'))

config={
    'development':DevelopmentConfig,
    'production':ProductionConfig,
    'testing':TestingConfig,
}