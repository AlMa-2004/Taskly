from app import db
from app.utils.timezone import now_ro

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)  # !! changed logic twice, each task should be assigned to a member
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=now_ro) # important for deadline logic
    due_date = db.Column(db.DateTime)
    status = db.Column(db.Enum('not allocated', 'in progress', 'done', 'overdue'), default='not allocated') # ! NEEDS REINFORCEMENT
    last_status_update = db.Column(db.DateTime, default=now_ro, onupdate=now_ro)

    member = db.relationship("Member", back_populates="tasks")

    # future concerns: if a task is unassigned/not allocated, it goes to a certain dummy user in the team
