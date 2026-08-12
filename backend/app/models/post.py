from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class PostBase(SQLModel):#common field shared
    title: str
    body: Optional[str] = None
    category_id: int


class Post(PostBase, table=True):#actual db table
    __tablename__ = "posts"

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int

    view_count: int = Field(default=0)

    is_pinned: bool = Field(default=False)
    is_locked: bool = Field(default=False)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


class PostCreate(PostBase):#data received
    pass


class PostPublic(PostBase):#data returned to fronted
    id: int
    user_id: int

    view_count: int

    is_pinned: bool
    is_locked: bool

    created_at: datetime
    updated_at: Optional[datetime]


class PostUpdate(SQLModel):#field that can be updated
    title: Optional[str] = None
    body: Optional[str] = None
    category_id: Optional[int] = None

    is_pinned: Optional[bool] = None
    is_locked: Optional[bool] = None