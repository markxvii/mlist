'''
项目初始化类
'''

import os

import click
from flask import Flask, render_template
from flask_login import current_user

from mlist.blueprints.auth import auth_bp
from mlist.blueprints.home import home_bp
from mlist.blueprints.todo import todo_bp
from mlist.extensions import db, login_manager, csrf,migrate
from mlist.models import User, Item
from mlist.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('mlist')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_template_context(app)
    return app


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app,db)


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(todo_bp)
    app.register_blueprint(home_bp)


def register_commands(app):
    @app.cli.command()
    @click.option('--drop',is_flag=True,help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('Will delete the database,CONTINUE?',abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('done.')


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors.html',code=400,info='Bad Request'),400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors.html', code=403, info='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors.html', code=404, info='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors.html', code=500, info='Server Error'), 500


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        if current_user.is_authenticated:
            active_items=Item.query.with_parent(current_user).filter_by(done=False).count()
        else:
            active_items=None
        return dict(active_items=active_items)
