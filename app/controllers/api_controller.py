# app/controllers/api_controller.py
from flask import Blueprint, jsonify
from datetime import datetime
from app.models.tasks import Task
from app import db

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/check-updates')
def check_updates():
    now = datetime.now() 
    tasks = Task.query.filter(
        Task.due_date < now,
        Task.status != 'done',
        Task.status != 'overdue'
    ).all()

    updated = False
    for task in tasks:
        task.status = 'overdue'
        updated = True

    if updated:
        db.session.commit()

    return jsonify({'updated': updated})
