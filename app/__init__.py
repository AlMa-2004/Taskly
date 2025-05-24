from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'placeholder') # a placeholder is needed for dev in case a secret key is not set/retreived. 
    # ! secret key => secure flask_login sessions and protect form => flask wtf

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # ! IMPORTANT (uncomment when merged with main branch)
    from app.models import users, teams, roles, members, tasks

    return app
