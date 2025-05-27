from app import db

class Member(db.Model):
    __tablename__ = 'members' # configuration line for sqlacl

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete='CASCADE'), nullable=False) # deleting a team will delete all members, a member has to be tied to a team
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False) # the deletion of a user will mean the deletion of a member, membership has to be tied to a user
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False) # a member MUST have a role
    joined_at = db.Column(db.DateTime, server_default=db.func.now())

    team = db.relationship("Team", back_populates="members") # it's not enough to define a foreign key with sqlalc, you have to link the models together in ORM logic
    user = db.relationship("User", back_populates="members")

    tasks = db.relationship("Task", back_populates="member", cascade="all, delete-orphan") # in case of deletion of a member, tasks will be also deleted