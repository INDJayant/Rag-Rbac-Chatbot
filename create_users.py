from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, RoleEnum

# Create sample users
def create_sample_users():
    db: Session = SessionLocal()
    users = [
        {"username": "admin1", "password": "adminpass", "role": RoleEnum.admin},
        {"username": "user1", "password": "userpass", "role": RoleEnum.user},
        {"username": "auditor1", "password": "auditpass", "role": RoleEnum.auditor},
    ]
    for u in users:
        user = User(**u)
        db.add(user)
    db.commit()
    db.close()
    print("Sample users created.")

create_sample_users()
