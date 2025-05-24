from flask import Blueprint, render_template #jsonify
from flask_login import login_required, current_user

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def home():
    user = current_user
    teams = [m.team.name for m in user.members]
    return render_template('dashboard.html', user=user, teams=teams)
    #return jsonify({'message': f'Welcome, {user.name}', 'teams': teams})