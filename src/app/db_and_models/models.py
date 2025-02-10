from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# base model for user data, used for data validation and transfer
class UserModel(SQLModel):
    username: str
    email: EmailStr
    password: str
    name: str


# database table for users, extends the base model and makes it a table
class UserTable(UserModel, table=True):
    __tablename__ = "users"  # explicit table name

    id: Optional[int] = Field(default=None, primary_key=True)

    # relationship to posts
    # - this creates a one-to-many relationship (one user → many posts)
    # - sqlmodel will not create a column for this, it is only used for accessing related posts
    # - back_populates="author" means it connects to the "author" attribute in PostTable
    posts: list["PostTable"] = Relationship(back_populates="author")


# base model for post data, used for validation and data transfer
class PostModel(SQLModel):
    content: str

    # defaults to current time
    created_at: datetime = Field(default_factory=datetime.now)


# database table for posts, extends PostModel and makes it a table
class PostTable(PostModel, table=True):
    __tablename__ = "posts"

    id: Optional[int] = Field(default=None, primary_key=True)

    # foreign key to link a post to a user
    # - this creates a column "user_id" in the posts table
    # - foreign_key="users.id" means it references the id column in the users table
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")

    # relationship back to the user who created the post
    # - this creates the "many-to-one" side of the relationship (many posts → one user)
    # - back_populates="posts" links back to the "posts" attribute in UserTable
    author: Optional[UserTable] = Relationship(back_populates="posts")
