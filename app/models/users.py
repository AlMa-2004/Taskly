# users.py
from app import db
from flask_login import UserMixin # helper class: adds session-related methods (is_authenticated, get_id) to the User model for flask login to work properly
from app.utils.timezone import now_ro

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(255))
    google_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=now_ro)

    members = db.relationship('Member', back_populates='user', cascade='all, delete-orphan') # with backref, the relationship is defined both ways

# Flask-login requires a User model with the following properties:

# has an is_authenticated() method that returns True if the user has provided valid credentials
# has an is_active() method that returns True if the user’s account is active
# has an is_anonymous() method that returns True if the current user is an anonymous user
# has a get_id() method which, given a User instance, returns the unique ID for that object

# UserMixin class provides the implementation of this properties.
