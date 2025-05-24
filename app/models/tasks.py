from app import db

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)  # !! Changed logic twice, each task should be assigned to a member
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    due_date = db.Column(db.DateTime)
    status = db.Column(db.Enum('not allocated', 'in progress', 'done', 'overdue'),default='not allocated') # ! NEEDS REINFORCEMENT
    last_status_update = db.Column(db.DateTime,server_default=db.func.now(),onupdate=db.func.now())

    member = db.relationship("Member", back_populates="tasks")

    # future concerns: if a task is unassigned/not allocated, it goes to a certain dummy user in the team
