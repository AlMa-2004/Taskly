from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from flask_login import login_required
from app.models.tasks import Task
from app import db

task_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@task_bp.route('/create', methods=['POST'])
@login_required
def create_task():
    description = request.form.get("description")
    member_id = request.form.get("member_id")
    due_date = request.form.get("due_date")
    team_id = request.form.get("team_id")

    if not description or not team_id:
        return "Missing fields", 400

    task = Task(
        description=description,
        member_id=member_id if member_id else None,
        due_date=due_date if due_date else None,
    )

    db.session.add(task)
    db.session.commit()
    return redirect(url_for('dashboard.admin_dashboard'))


@task_bp.route('/<int:task_id>', methods=['GET'])
@login_required
def view_task(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('task_detail.html', task=task)