# app/controllers/api_controller.py
from flask import Blueprint, jsonify
from datetime import datetime
import pytz
from app.models.tasks import Task
from app import db

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/check-updates')
def check_updates():
    overdue_tasks = Task.query.filter(Task.status == 'overdue').count()
    return jsonify({'updated': overdue_tasks > 0})
