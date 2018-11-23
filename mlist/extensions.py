'''
组件类
'''

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

db=SQLAlchemy()
csrf=CSRFProtect()
migrate=Migrate()

login_manager=LoginManager()
login_manager.login_view='auth.login'

@login_manager.user_loader
def load_user(user_id):
    from mlist.models import User
    return User.query.get(int(user_id))