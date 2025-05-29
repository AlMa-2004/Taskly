from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import pytz
from app.models.tasks import Task
from app import db

RO_TZ = pytz.timezone('Europe/Bucharest')

def check_and_clean_tasks():
    now = datetime.now(RO_TZ)

    tasks = Task.query.filter(
        Task.due_date < now,
        Task.status != 'done',
        Task.status != 'overdue'
    ).all()
    for task in tasks:
        task.status = 'overdue'

    cutoff = now - timedelta(days=1)
    old_tasks = Task.query.filter(
        Task.status == 'overdue',
        Task.due_date < cutoff
    ).all()

    for task in old_tasks:
        db.session.delete(task)

    if tasks or old_tasks:
        db.session.commit()
        print(f"[{now}] --------> Updated {len(tasks)} tasks, deleted {len(old_tasks)}.")

def init_scheduler(app):
    scheduler = BackgroundScheduler()

    def scheduled_job():
        with app.app_context():
            check_and_clean_tasks()

    scheduler.add_job(func=scheduled_job, trigger="interval", minutes=1)
    scheduler.start()
