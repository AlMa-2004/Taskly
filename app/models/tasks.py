from app import db

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    due_date = db.Column(db.DateTime)
    status = db.Column(db.Enum('not allocated', 'in progress', 'done', 'overdue'), default='not allocated') # ! NEEDS REINFORCEMENT WITHIN THE APP
    last_status_update = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    team = db.relationship("Team", back_populates="tasks")
