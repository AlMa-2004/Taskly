from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import login_required, current_user
from app.models.roles import Role

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.members or len(current_user.members) == 0:
        return redirect(url_for('teams.choose_team_option'))

    # Check if user is Admin in any team
    for member in current_user.members:
        if member.role.name == 'Admin':
            return redirect(url_for('dashboard.admin_dashboard'))

    tasks = []
    for m in current_user.members:
        tasks.extend(m.tasks)

    return render_template('dashboard.html', user=current_user, tasks=tasks)


@dashboard_bp.route('/dashboard/admin')
@login_required
def admin_dashboard():

    if not current_user.members:
        return redirect(url_for('teams.choose_team_option'))
    # for simplicity, a user is only managing one team, although the db supports multiple teams.
    member = current_user.members[0]
    if member.role.name != 'Admin':
        return abort(403)  #forbidden

    team = member.team

    assigned_tasks = []
    for m in team.members:
        assigned_tasks.extend(
            [task for task in m.tasks if task.member_id == member.id]
        )

    return render_template('admin_dashboard.html', team=team, assigned_tasks=assigned_tasks)