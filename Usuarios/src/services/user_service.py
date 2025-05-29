from sqlalchemy.orm import Session
from ..models.user import User

def get_user_profile(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user_profile(db: Session, user_id: int, **kwargs):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("Usuario no encontrado")
    
    for key, value in kwargs.items():
        setattr(user, key, value)
    db.commit()
    return user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email.ilike(email)).first()

