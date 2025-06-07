# team_controller.py
from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.teams import Team
from app.models.members import Member
from app.models.roles import Role
from app.models.users import User
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

    # creates the dummy user (unassigned tasks) upon team creation
    unassigned_user = User.query.filter_by(email='unassigned@system.local').first()
    if not unassigned_user:
        unassigned_user = User(
            name='Unassigned',
            surname='',
            email='unassigned@system.local',
            password='', 
            google_id='unassigned'
        )
        db.session.add(unassigned_user)
        db.session.commit()

    unassigned_role = Role.query.filter_by(name='Viewer').first()  #lowest permissions
    unassigned_member = Member(
        user_id=unassigned_user.id,
        team_id=team.id,
        role_id=unassigned_role.id
    )
    db.session.add(unassigned_member)
    db.session.commit()

    return redirect(url_for('dashboard.dashboard'))

@team_bp.route('/join', methods=['POST'])
@login_required
def process_join():
    invite_code = request.form.get('invite_code')
    
    if not invite_code:
        return "Invite code is required.", 400

    team = Team.query.filter_by(invite_code=invite_code).first()
    if not team:
        return "Invalid invite code.", 404

    from app.models.roles import Role
    role = Role.query.filter_by(name='Member').first() # gets role id from Roles table

    member = Member(user_id=current_user.id, team_id=team.id, role_id=role.id)
    db.session.add(member)
    db.session.commit()

    return redirect(url_for('dashboard.dashboard'))
