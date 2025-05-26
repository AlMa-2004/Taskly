from app import db

class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    joined_at = db.Column(db.DateTime, server_default=db.func.now())

    team = db.relationship("Team", back_populates="members")
    user = db.relationship("User", back_populates="members")

    tasks = db.relationship("Task", back_populates="member", cascade="all, delete-orphan") 