from sqlalchemy.orm import Session
from ..models.user import User
from ..utils.security import get_password_hash, verify_password

#falta las funciones get_password_hash, verify_password en security
def register_user(db: Session, user_data):
    if db.query(User).filter(User.email == user_data.email).first():
        raise ValueError("El email ya está registrado")
    
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        nombre=user_data.nombre,
        apellido=user_data.apellido,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None