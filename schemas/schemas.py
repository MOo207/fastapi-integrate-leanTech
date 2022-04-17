from typing import List, Optional
from email_validator import validate_email, EmailNotValidError

from pydantic import BaseModel, EmailStr, Extra, validator
from pydantic.dataclasses import dataclass

class UserBase(BaseModel):
    email: str
    password: str
    
class UserCreate(BaseModel):
    email: str
    password: str

class SignupUser(UserBase):
    email: EmailStr 
    password: str
    confirm_password: str
    @validator('email')
    def email_validator(cls, v):
        if validate_email(v):
            raise ValueError('Check your email')
        return v.title()

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v

class LoginUser(UserBase):
    email: str
    password: str
    class Config:
        extra = Extra.forbid

class User(UserBase):
    id: int
    email: str
    class Config:
        orm_mode = True


class LeanBase(BaseModel):
    user_id: int

class LeanCreateCustomer(LeanBase):
    user_id: int

class LeanUserLink(UserBase):
    user_id: int
    app_user_id: str
    customer_id: str

class User(UserBase):
    id: int
    email: str
    class Config:
        orm_mode = True