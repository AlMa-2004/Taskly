from flask import Blueprint, request, render_template, jsonify
from flask_login import login_required
from app.models.tasks import Task
from app import db

task_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@task_bp.route('/create', methods=['POST'])
@login_required
def create_task():
    data = request.json
    task = Task(
        member_id=data.get('member_id'),
        description=data.get('description'),
        due_date=data.get('due_date')
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({'status': 'task created', 'task_id': task.id})

@task_bp.route('/<int:task_id>', methods=['GET'])
@login_required
def view_task(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('task_detail.html', task=task)