import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

from app import create_app, db
from app.models.users import User
from app.models.teams import Team
from app.models.members import Member
from app.models.tasks import Task

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    user = User(name='Test', surname='User', email='test@example.com', google_id='abc123')
    db.session.add(user)
    db.session.commit()

    team = Team(name='Dev Team')
    db.session.add(team)
    db.session.commit()

    member = Member(user_id=user.id, team_id=team.id)
    db.session.add(member)
    db.session.commit()

    task = Task(description='Initial task', member_id=member.id)
    db.session.add(task)
    db.session.commit()

    print("The test has been successful!")
