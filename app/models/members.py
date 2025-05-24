from app import db

class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    joined_at = db.Column(db.DateTime, server_default=db.func.now())

    team = db.relationship("Team", back_populates="members")
    user = db.relationship("User", back_populates="members")
    role = db.relationship("Role", back_populates="members")
