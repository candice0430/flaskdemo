from ext import db
from datetime import datetime


class EmailCapatureModel(db.Model):
    __tablename__ = 'email_capture'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    capture = db.Column(db.String(100),nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)


class UserModel(db.Model):
    __tablename__ ='user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=False, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=False)

