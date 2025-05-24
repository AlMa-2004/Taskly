from app import db

class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    members = db.relationship("Member", back_populates="team")
    tasks = db.relationship("Task", back_populates="team")

    # Needed for a custom join! Since tasks are only attached to its members
    tasks = db.relationship(
        "Task",
        secondary="members",  # intermediate table
        primaryjoin="Team.id==Member.team_id",
        secondaryjoin="Member.id==Task.member_id",
        viewonly=True
    )