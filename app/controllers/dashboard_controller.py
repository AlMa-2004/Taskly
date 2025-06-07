# dashboard_controller.py
from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import login_required, current_user
from app.models.members import Member
from app.models.users import User
from app.models.tasks import Task
from app.models.users import User

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.members:
        return redirect(url_for('teams.choose_team_option'))

    # redirect admins
    for m in current_user.members:
        if m.role.name == 'Admin':
            return redirect(url_for('dashboard.admin_dashboard'))

    tasks = []

    # my assigned tasks from all teams (supported in the future), for simplicity, the user belongs to one team for now
    for m in current_user.members:
        tasks.extend(m.tasks)

    # include unassigned tasks from team by introducing a special dummy user
    unassigned_user = User.query.filter_by(email='unassigned@system.local').first()
    if unassigned_user:
        for m in current_user.members:
            unassigned_member = Member.query.filter_by(user_id=unassigned_user.id, team_id=m.team_id).first()
            if unassigned_member: # if found, fetch their tasks (unassigned tasks) and include them
                unassigned_tasks = Task.query.filter_by(member_id=unassigned_member.id).all()
                tasks.extend(unassigned_tasks)

    return render_template('dashboard.html', user=current_user, tasks=tasks) # parameter needed to the jinja template

@dashboard_bp.route('/dashboard/admin')
@login_required
def admin_dashboard():
    admin_member = None
    for m in current_user.members:
        if m.role.name == 'Admin':
            admin_member = m
            break

    if not admin_member:
        return abort(403)

    team = admin_member.team

    # all tasks from all team members
    all_tasks = []
    for m in team.members:
        all_tasks.extend(m.tasks)

    # show unassigned member
    unassigned_user = User.query.filter_by(email='unassigned@system.local').first()
    unassigned_member = Member.query.filter_by(user_id=unassigned_user.id, team_id=team.id).first()

    return render_template(
        'admin_dashboard.html',
        team=team,
        all_tasks=all_tasks,
        own_tasks=admin_member.tasks,
        unassigned_member=unassigned_member
    )