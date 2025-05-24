from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.teams import Team
from app.models.members import Member
from app.models.roles import Role
from app import db

team_bp = Blueprint('teams', __name__, url_prefix='/teams')

@team_bp.route('/create', methods=['GET'])
@login_required
def create_team_form():
    return render_template('create_team.html')

@team_bp.route('/choose', methods=['GET'])
@login_required
def choose_team_option():
    return render_template('choose_team.html')

@team_bp.route('/create', methods=['POST'])
@login_required
def create_team():
    name = request.form.get('name')
    if not name:
        return "Team name is required", 400

    team = Team(name=name)
    db.session.add(team)
    db.session.commit()

    admin_role = Role.query.filter_by(name='Admin').first()
    if not admin_role:
        return "Admin role not found. OOPS!", 500

    member = Member(user_id=current_user.id, team_id=team.id, role_id=admin_role.id)
    db.session.add(member)
    db.session.commit()

    return redirect(url_for('dashboard.dashboard'))
