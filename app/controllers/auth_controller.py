from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from firebase_admin import auth as firebase_auth
from flask_login import login_user, logout_user
from app.models.users import User
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login/google', methods=['POST'])
def google_login():
    id_token = request.json.get('idToken')
    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        email = decoded_token.get('email')
        name = decoded_token.get('name')

        user = User.query.filter_by(google_id=uid).first()
        if not user:
            user = User(google_id=uid, email=email, name=name, surname='', password='')
            db.session.add(user)
            db.session.commit()

        login_user(user)
        return jsonify({'status': 'success'}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 401

@auth_bp.route('/logout')
def logout():
    logout_user()
    #return jsonify({'status': 'logged out'})
    return redirect(url_for('auth.login_page'))

@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')