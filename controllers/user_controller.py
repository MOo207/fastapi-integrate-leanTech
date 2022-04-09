from sqlalchemy.orm import Session
from models import models

from passlib.context import CryptContext

from models.schemas import User, UserCreate, UserLeanBind
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_email_and_password(db: Session, email: str, password: str):
    user: User = db.query(models.User).filter(models.User.email == email).first()
    if user and pwd_context.verify(password, user.hashed_password):
        return user
    else:
        return False


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return "User deleted"


def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: UserCreate):
    print(user.customer_id)
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.query(User).filter(models.User.id == user_id).update(user.dict())
        db.commit()
        return user
    else:
        return "User not found"

# def bind_user_lean(db: Session, user_id: int, user: UserLeanBind):
#     print(user.app_user_id)
#     db_user: UserAllAttr = db.query(models.User).filter(models.User.id == user_id).first()
#     print(db_user.dict)
#     # if db_user:
#     #     db_user.customer_id = user.customer_id
#     #     db_user.app_user_id = user.app_user_id
#     #     db.query(User).filter(models.User.id == user_id).update(db_user.dict())
#     #     db.commit()
#     #     return user
#     # else:
#     #     return "User not found"
