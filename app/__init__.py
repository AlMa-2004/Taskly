from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import credentials

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

    from app.controllers.auth_controller import auth_bp
    from app.controllers.team_controller import team_bp
    from app.controllers.task_controller import task_bp
    from app.controllers.dashboard_controller import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(team_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(dashboard_bp)

    cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH', 'firebase/firebase-adminsdk.json')
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

    from app.models.users import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id)) # for flask-login; retreives the current user from the session

    return app
