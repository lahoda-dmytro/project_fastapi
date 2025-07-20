from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
from .role import user_roles


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    age = Column(Integer)
    hashed_password = Column(String, nullable=True)
    roles = relationship('Role', secondary=user_roles, back_populates='users')
    posts = relationship('Post', back_populates='author')
