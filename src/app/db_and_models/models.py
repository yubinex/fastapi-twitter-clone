from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class UserFollowerLink(SQLModel, table=True):
    __tablename__ = "user_follower_link"

    # composite primary key consisting of `user_id` and `follower_id`
    # - `user_id` references `users.id` (the user being followed)
    # - `follower_id` references f`ollowers.id` (the user who is following)
    # - together they form the many-to-many relationship between users and followers
    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    follower_id: Optional[int] = Field(
        default=None, foreign_key="followers.id", primary_key=True
    )


# base model for user data, used for data validation and transfer
class UserModel(SQLModel):
    username: str
    email: EmailStr
    password: str
    name: str


# database table for users, extends the base model and makes it a table
class User(UserModel, table=True):
    __tablename__ = "users"  # explicit table name

    id: Optional[int] = Field(default=None, primary_key=True)

    # relationship to posts
    # - this creates a one-to-many relationship (one user → many posts)
    # - sqlmodel will not create a column for this, it is only used for accessing related posts
    # - back_populates="author" means it connects to the "author" attribute in PostTable
    posts: list["Post"] = Relationship(back_populates="author")
    likes: list["Like"] = Relationship(back_populates="user")

    # relationship to followers through the association table
    # - creates a many-to-many relationship between users and followers
    # - link_model=UserFollowerLink specifies the junction table
    # - back_populates connects to "followed_users" in Follower
    # - allows accessing `user.followers` to get all their followers
    followers: list["Follower"] = Relationship(
        back_populates="followed_users", link_model=UserFollowerLink
    )


# base model for post data, used for validation and data transfer
class PostModel(SQLModel):
    content: str

    # defaults to current time
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


# database table for posts, extends PostModel and makes it a table
class Post(PostModel, table=True):
    __tablename__ = "posts"

    id: Optional[int] = Field(default=None, primary_key=True)

    # foreign key to link a post to a user
    # - this creates a column "user_id" in the posts table
    # - foreign_key="users.id" means it references the id column in the users table
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")

    # relationship back to the user who created the post
    # - this creates the "many-to-one" side of the relationship (many posts → one user)
    # - back_populates="posts" links back to the "posts" attribute in UserTable
    author: Optional[User] = Relationship(back_populates="posts")
    likes: list["Like"] = Relationship(back_populates="post")


class LikeModel(SQLModel):
    post_id: Optional[int] = Field(default=None, foreign_key="posts.id")


class Like(LikeModel, table=True):
    __tablename__ = "likes"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")

    user: Optional[User] = Relationship(back_populates="likes")
    post: Optional[Post] = Relationship(back_populates="likes")


class FollowerModel(SQLModel):
    follower_id: int


class Follower(FollowerModel, table=True):
    __tablename__ = "followers"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int

    # relationship back to users through the association table
    # - relative side of the many-to-many relationship
    # - link_model=UserFollowerLink connects using the same junction table
    # - back_populates connects to "followers" in user
    # - allows accessing `follower.followed_users` to get all followed accounts
    followed_users: list[User] = Relationship(
        back_populates="followers", link_model=UserFollowerLink
    )
