from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from app.models.tasks import Task
from app.models.members import Member
from app.models.users import User
from app import db

task_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@task_bp.route('/create', methods=['POST'])
@login_required
def create_task():
    # extract task data from form
    description = request.form.get("description")
    member_id = request.form.get("member_id")
    due_date = request.form.get("due_date")
    team_id = request.form.get("team_id")

    if not description or not team_id:
        return "Missing fields", 400

    # Retrieve the special 'unassigned' user
    unassigned_user = User.query.filter_by(email='unassigned@system.local').first()
    if not unassigned_user:
        return "Unassigned user missing", 500

    # find the 'unassigned' member in the current team
    unassigned_member = Member.query.filter_by(
        user_id=unassigned_user.id,
        team_id=team_id
    ).first()

    due_date_raw = request.form.get("due_date")
    try:
        due_date = datetime.strptime(due_date_raw, "%Y-%m-%dT%H:%M")
        # change to 23:59 for full-day tasks if the time is not specified in the from
        if due_date.time().hour == 0 and due_date.time().minute == 0:
            due_date = due_date.replace(hour=23, minute=59)
    except (ValueError, TypeError):
        return "Invalid date format", 400

    if not unassigned_member:
        return "Unassigned member not found for this team", 500

    task = Task(
        description=description,
        member_id=member_id if member_id else None,
        due_date=due_date if due_date else None,
        status='not allocated' if str(member_id) == str(unassigned_member.id) else 'in progress'
    )

    # saves to the database
    db.session.add(task)
    db.session.commit()

    return redirect(url_for('dashboard.admin_dashboard'))

@task_bp.route('/pick-up', methods=['POST'])
@login_required
def pick_up_task():
    task_id = request.form.get('task_id')
    task = Task.query.get(task_id)

    # validate task exists and is unassigned
    if not task or not task.member or task.member.user.name != 'Unassigned':
        return "Task not available for pickup.", 403

    # find the current user's member for the task's team
    team_id = task.member.team_id
    member = Member.query.filter_by(user_id=current_user.id, team_id=team_id).first()
    if not member:
        return "You are not a member of this team.", 403

    # assign the task to the user and mark as in progress
    task.member_id = member.id
    task.status = 'in progress'
    db.session.commit()

    return redirect(url_for('dashboard.dashboard'))

# route to update the status of a task, <> => dynamic url parameter, passes it to the function
@task_bp.route('/<int:task_id>/update-status', methods=['POST'])
@login_required
def update_status(task_id):
    new_status = request.form.get('status')
    task = Task.query.get_or_404(task_id)

    # make sure the task belongs to the current user
    member_ids = [m.id for m in current_user.members]
    if task.member_id not in member_ids:
        return "Unauthorized", 403

    # only allow VALID status updates, even though there is an overdue option, reinforced in next functions
    if new_status not in ['in progress', 'done']:
        return "Invalid status", 400

    # cannot change from 'overdue' to 'in progress'
    if task.status == 'overdue' and new_status != 'done':
        return "You cannot revert an overdue task to 'in progress'.", 403

    if new_status == 'overdue':
        return "Overdue status is system-assigned only.", 403
    
    task.status = new_status
    db.session.commit()
    return redirect(url_for('dashboard.dashboard'))

# (admin-only) task deletion
@task_bp.route('/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    # make sure task is assigned to a valid member
    if not task.member:
        return "This task is not assigned to a valid member.", 400

    task_team_id = task.member.team_id

    # check if current user is an Admin in the task's team
    is_admin = any(
        m.team_id == task_team_id and m.role.name == 'Admin'
        for m in current_user.members
    )

    if not is_admin:
        return "Unauthorized", 403

    # delete task from database
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('dashboard.admin_dashboard'))
