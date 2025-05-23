from sqlalchemy.orm import Session
from ..models.user import User
from ..utils.security import get_password_hash, verify_password
from sqlalchemy.orm import Session, joinedload
from ..models.user import User
from ..utils.security import get_password_hash, verify_password
from ..schemas.user import UserCreate
from ..models.role import Role


def register_user(db: Session, user_data: UserCreate):
    # Verifica si el email ya está registrado
    if db.query(User).filter(User.email == user_data.email).first():
        raise ValueError("El email ya está registrado")
    
    # Asegúrate de que el valor de 'role' sea un valor válido de 'RoleName'
    role = db.query(Role).filter(Role.name == user_data.role).first()  # Ahora buscamos el rol en la base de datos
    if not role:
        raise ValueError("Rol no encontrado")  # Si el rol no se encuentra en la base de datos
    
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        nombre=user_data.nombre,
        apellido=user_data.apellido,
        hashed_password=hashed_password,
        role_id=role.id  # Almacenamos el ID del rol
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).options(joinedload(User.role)).filter(User.email == email).first()
    
    if not user or not verify_password(password, user.hashed_password):
        return None
    
    return user