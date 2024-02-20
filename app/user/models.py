from typing import Optional, List

from sqlmodel import Field, SQLModel, Relationship


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: Optional[int] = None

    books: List["Book"] = Relationship(back_populates="user")


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: Optional[int] = None

    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="books")
