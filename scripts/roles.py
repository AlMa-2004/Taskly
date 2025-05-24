import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

from app import create_app, db
from app.models.roles import Role

app = create_app()

with app.app_context():
    if not Role.query.first():
        roles = [
            Role(
                name='Admin',
                can_delete_team=True,
                can_edit_task=True,
                can_delete_task=True,
                can_assign_task=True,
                can_unassign_task=True,
                can_pick_up=True
            ),
            Role(
                name='Member',
                can_delete_team=False,
                can_edit_task=True,
                can_delete_task=False,
                can_assign_task=False,
                can_unassign_task=False,
                can_pick_up=True
            ),
            Role(
                name='Viewer',
                can_delete_team=False,
                can_edit_task=False,
                can_delete_task=False,
                can_assign_task=False,
                can_unassign_task=False,
                can_pick_up=False
            ),
        ]
        db.session.add_all(roles)
        db.session.commit()
        print("Roles created successfully.")
    else:
        print("Roles already exist. Skipping...")
