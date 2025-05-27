from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import credentials

# instantiate flask extensions globally so they can be initialized later
db = SQLAlchemy() # for ORM logic
migrate = Migrate() # handles database migrations
login_manager = LoginManager() # for user sessions management

def create_app():
    # loads environment variables from a .env file
    load_dotenv()

    # create the main flask app instance
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') # database connection string
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'placeholder') # used to secure session cookies; 'placeholder' as fallback

    # initialize the extensions with the app instance as a parameter
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # import models so flask migrate can detect them
    from app.models import users, teams, roles, members, tasks

    # import all blueprint route controllers
    from app.controllers.auth_controller import auth_bp
    from app.controllers.team_controller import team_bp
    from app.controllers.task_controller import task_bp
    from app.controllers.dashboard_controller import dashboard_bp
    from app.controllers.api_controller import api_bp
    from app.controllers.main_controller import main_bp

    # register each blueprint with the app (organizes your routes by module)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(team_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(main_bp)

    # initialize Firebase Admin SDK using private key
    cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH', 'firebase/firebase-adminsdk.json')
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

    # user loader for flask login => tells flask how to get a user id ! it is NECCESARY to have it defined
    from app.models.users import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # retrieves user from daabase for session tracking

    # initialize background scheduler
    from app.scheduler import init_scheduler
    init_scheduler(app)

    # return the fully configured app object
    return app
