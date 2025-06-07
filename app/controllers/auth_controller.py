# auth_controller.py
from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from firebase_admin import auth as firebase_auth
from flask_login import login_user, logout_user
from app.models.users import User
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth') # for modularity and scalability

# the route will always have a prefix given by the blueprint
# a route can respond to multiple http methods/requests, so it has to be stated which one it corresponds to
# so, multiple methods => string vector for each one (here it has one element)
@auth_bp.route('/login/google', methods=['POST']) 
def google_login():
    id_token = request.json.get('idToken') # the frontend sends a token in json format, this is where it is received in the backend
    try:
        decoded_token = firebase_auth.verify_id_token(id_token) # the token gets decoded and verified (with parameters from )

        # takes info decoded token
        uid = decoded_token['uid']
        email = decoded_token.get('email')
        name = decoded_token.get('name')

        user = User.query.filter_by(google_id=uid).first() # if the user doesn't exist in the db's userss table, it creates it
        if not user:
            user = User(google_id=uid, email=email, name=name, surname='', password='') # for now, password is only stored in firebase
            db.session.add(user)
            db.session.commit()

        login_user(user) # function provided by flask login => now the logged user can be identified through "current_user"
        return jsonify({'status': 'success'}), 200

    except Exception as e: # if the token is invalid (could mean not real, expired), the login is unsuccesful
        return jsonify({'status': 'error', 'message': str(e)}), 401

@auth_bp.route('/logout')
def logout():
    logout_user() # ends the user session through flask login lib
    #return jsonify({'status': 'logged out'})
    return redirect(url_for('auth.login_page'))

@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')