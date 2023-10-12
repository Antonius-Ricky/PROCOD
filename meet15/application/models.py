from application import db
from flask import Flask
from sqlalchemy.sql import func

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    photoprofile = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    comments = db.relationship('Comment', back_populates='user')
    posts = db.relationship('Post', back_populates='user')
    likes = db.relationship('Like', back_populates='user')
    
    followers = db.relationship('Relationship', foreign_keys='Relationship.following_id', back_populates='following')
    following = db.relationship('Relationship', foreign_keys='Relationship.follower_id', back_populates='follower')

class Relationship(db.Model):
    __tablename__ = 'relationships'
    
    relationship_id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    following_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    follower = db.relationship('User', foreign_keys=[follower_id], back_populates='followers')
    following = db.relationship('User', foreign_keys=[following_id], back_populates='following')

class Comment(db.Model):
    __tablename__ = 'comments'
    
    comment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    user = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')

class Post(db.Model):
    __tablename__ = 'posts'
    
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    photo = db.Column(db.String(255))
    caption = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    user = db.relationship('User', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post')
    likes = db.relationship('Like', back_populates='post')

class Like(db.Model):
    __tablename__ = 'likes'
    
    like_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    user = db.relationship('User', back_populates='likes')
    post = db.relationship('Post', back_populates='likes')