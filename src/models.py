import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Users(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

    comments = relationship('Comments', backref='user', lazy=True)
    posts = relationship('Posts', backref='user', lazy=True)

    followers = relationship('Followers', foreign_keys='Followers.following_id', backref='following', lazy=True)
    following = relationship('Followers', foreign_keys='Followers.follower_id', backref='followers', lazy=True) 
    
class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))

    comments = relationship('Comments', backref='post', lazy=True)
    media = relationship('Media', secondary='PostMediaConnectio', lazy='subquery', backref= 'posts')

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    url = Column(String(250), nullable=False)

class PostMediaConnection(Base):
    __tablename__ = 'post_media_connection'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    media_id = Column(Integer, ForeignKey('media.id'))



class Followers(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('user.id'))
    following_id = Column(Integer, ForeignKey('user.id'))
    
class Comments(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))


    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
