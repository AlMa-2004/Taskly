# teams.py
from app import db
from secrets import token_urlsafe
from app.utils.timezone import now_ro

class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=now_ro)
    invite_code = db.Column(db.String(20), unique=True, default=lambda: token_urlsafe(8)) # generated invitation code, high probabilty to be unique

    members = db.relationship('Member', back_populates='team', cascade='all, delete-orphan')

    # custom join => since tasks are only attached to its members, this is how the viewing of tasks per team is done
    tasks = db.relationship(
        "Task",
        secondary="members",  # intermediate table
        primaryjoin="Team.id==Member.team_id",
        secondaryjoin="Member.id==Task.member_id",
        viewonly=True
    )
