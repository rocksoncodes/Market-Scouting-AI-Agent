from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database.base import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    submission_id = Column(String(20), unique=True, nullable=False)
    subreddit = Column(String(100), nullable=False)
    title = Column(Text, nullable=False)
    body = Column(Text)
    upvote_ratio = Column(Float)
    score = Column(Integer)
    is_processed = Column(Boolean, default=False)

    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    submission_id = Column(String(20), ForeignKey("posts.submission_id"))
    subreddit = Column(String(100), nullable=False)
    title = Column(Text, nullable=False)
    author = Column(String(255))
    body = Column(Text)
    score = Column(Integer)

    post = relationship("Post", back_populates="comments")
