from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class UserBase(SQLModel): #all user infos
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    avatar_url: Optional[str] = None
    bio: Optional[str] = None

class User(UserBase, table=True): #
    __tablename__ = "User"
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str
    role: str = Field(default="user")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase): #input plain password is hashed
    password: str

class UserPublic(UserBase): #api sends these
    id: int
    role: str
    created_at: datetime

class UserUpdate(SQLModel): #to update them
    username: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    password: Optional[str] = None