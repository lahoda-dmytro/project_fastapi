from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import base

user_roles = Table(
    'user_roles',
    base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)


class User(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    age = Column(Integer)
    hashed_password = Column(String, nullable=True)  # nullable=Truenullable=Truenullable=Truenullable=True
    roles = relationship('Role', secondary=user_roles, backref='user')


class Post(base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'))

    author = relationship('User')


class Role(base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
