from flask import Blueprint, render_template
from flask_login import login_required, current_user

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    tasks = []
    for m in current_user.members:
        tasks.extend(m.tasks)

    return render_template('dashboard.html', user=current_user, tasks=tasks)
