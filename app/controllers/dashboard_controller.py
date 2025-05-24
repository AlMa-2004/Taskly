from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    tasks = []
    if not current_user.members or len(current_user.members) == 0:
        return redirect(url_for('teams.choose_team_form'))

    for m in current_user.members:
        tasks.extend(m.tasks)

    return render_template('dashboard.html', user=current_user, tasks=tasks)

