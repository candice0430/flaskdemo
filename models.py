from ext import db
from datetime import datetime


class EmailCapatureModel(db.Model):
    __tablename__ = 'email_capture'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    captcha = db.Column(db.String(100), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=False, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class QuestionModel(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(1000), unique=False, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship('UserModel', backref=db.backref('articles'))
    create_time = db.Column(db.DateTime, default=datetime.now)


class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text(1000), unique=False, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    author = db.relationship('UserModel', backref=db.backref('comments'))
    qa = db.relationship('QuestionModel', backref=db.backref('comments'))
    create_time = db.Column(db.DateTime, default=datetime.now)
