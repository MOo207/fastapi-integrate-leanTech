from enum import unique
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class LeanUser(Base):
    __tablename__ = "lean_users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")

    customer_id = Column(String, unique=True, index=True)
    entity_id = Column(String, unique=True, index=True)
    app_user_id = Column(String, unique=True, index=True)