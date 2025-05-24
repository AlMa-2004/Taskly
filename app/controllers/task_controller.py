from flask import Blueprint, request, jsonify
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
