from app import create_app, db
from app.models.tasks import Task
from datetime import datetime

app = create_app()
app.app_context().push()

now = datetime.utcnow()
tasks = Task.query.filter(
    Task.due_date < now,
    Task.status != 'done',
    Task.status != 'overdue'
).all()

for task in tasks:
    task.status = 'overdue'

if tasks:
    db.session.commit()
    print(f"Updated {len(tasks)} overdue tasks.")
    with open("task_log.txt", "a") as f:
        f.write(f"[{datetime.utcnow()}]  Overdue check complete.\n")

else:
    print("No tasks to update.")
