# app/controllers/api_controller.py
from flask import Blueprint, jsonify
from datetime import datetime
import pytz
from app.models.tasks import Task
from app import db

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/check-updates')
def check_updates():
    overdue_tasks = Task.query.filter(Task.status == 'overdue').order_by(Task.last_status_update.desc()).all()
    latest_update = overdue_tasks[0].last_status_update.isoformat() if overdue_tasks else None
    return jsonify({
        'updated': bool(overdue_tasks),
        'latest_update': latest_update
    })
