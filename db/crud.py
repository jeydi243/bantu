from sqlalchemy.orm import Session
from . import models

def get_or_create_user(db: Session, user_id: int, first_name: str, last_name: str, username: str):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        db_user = models.User(
            id=user_id,
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user
