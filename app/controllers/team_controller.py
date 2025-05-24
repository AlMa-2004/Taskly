from flask import Blueprint, request, render_template, jsonify
from flask_login import login_required, current_user
from app.models.teams import Team
from app.models.members import Member
from app import db

team_bp = Blueprint('teams', __name__, url_prefix='/teams')

@team_bp.route('/create', methods=['POST'])
@login_required
def create_team():
    name = request.json.get('name')
    team = Team(name=name)
    db.session.add(team)
    db.session.commit()

    member = Member(user_id=current_user.id, team_id=team.id)
    db.session.add(member)
    db.session.commit()

    return jsonify({'status': 'created', 'team_id': team.id})


@team_bp.route('/<int:team_id>', methods=['GET'])
@login_required
def view_team(team_id):
    team = Team.query.get_or_404(team_id)
    members = team.members
    return render_template('team.html', team=team, members=members)