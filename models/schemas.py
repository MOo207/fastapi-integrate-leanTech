import email
from typing import List, Optional
from uuid import uuid4
from fastapi import Form

from pydantic import BaseModel, Extra
from pydantic.dataclasses import dataclass

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    email: str
    password: str
 
class UserLeanBind(UserBase):
    customer_id = str
    app_user_id = str

class UserLeanEntityUpdate(UserBase):
    entity_id = str


class User(UserBase):
    id: int
    email: str
    hashed_password: str
    customer_id: Optional[str]
    entity_id: Optional[str]
    app_user_id: Optional[str]
    class Config:
     use_enum_values = True