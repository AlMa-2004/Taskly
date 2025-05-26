from app import db

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    can_delete_task = db.Column(db.Boolean)
    can_assign_task = db.Column(db.Boolean)
    can_pick_up = db.Column(db.Boolean)

    members = db.relationship('Member', backref='role')
