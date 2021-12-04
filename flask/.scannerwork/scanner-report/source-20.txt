from flask import Flask, redirect, url_for, flash
from flask_login import LoginManager
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#local import
from config import app_config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize MySQL
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
     
    # blueprint for auth routes
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth routes
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    migrate = Migrate(app, db)
    from pms import models

    @app.before_first_request
    def before_first_request():
        try:
            user = models.Users.query.filter_by(username='expiredPassword').first()
        except:
            flash('Servie not reachable. Try again later.')
            return redirect(url_for('auth.login'))
        if(user == None):
            try:
                notMatchingPwCriteria = models.Users(username='notMatchingPwCriteria',password='pw', pw_expire_date='2050-12-04 00:09:20')
                expiredPassword = models.Users(username='expiredPassword', password='Password1!', pw_expire_date='2019-12-04 00:09:20')
                db.session.add(notMatchingPwCriteria)
                db.session.add(expiredPassword)
                db.session.commit()
            except:
                flash('Servie not reachable. Try again later.')
                return redirect(url_for('auth.login'))

    return app
