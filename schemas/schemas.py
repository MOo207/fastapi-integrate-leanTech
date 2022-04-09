import email
from typing import List, Optional
from uuid import uuid4
from fastapi import Form

from pydantic import BaseModel, Extra
from pydantic.dataclasses import dataclass

class UserBase(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    email: str
    password: str
    class Config:
        extra = Extra.forbid

class User(UserBase):
    id: int
    email: str
    class Config:
        orm_mode = True