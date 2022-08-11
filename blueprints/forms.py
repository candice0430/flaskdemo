from flask_wtf import FlaskForm
from flask import session
from wtforms import StringField
from wtforms.validators import length, InputRequired, equal_to, email, DataRequired, ValidationError
from ext import db
from models import UserModel,EmailCapatureModel
from werkzeug.security import generate_password_hash,check_password_hash


class RegisterForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(), length(min=6,max=20)])
    email = StringField("email", validators=[DataRequired(), email()])
    password = StringField(validators=[InputRequired(),length(min=6,max=20)])
    password_confirm = StringField(validators=[InputRequired(), equal_to('password', message='Passwords must match')])
    captcha = StringField("captcha", validators=[length(min=4,max=4)])

    def validate_username(self, field):
        if len(field.data) < 6:
            raise ValidationError('Name must be less than 50 characters')

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        capture_model = EmailCapatureModel.query.filter_by(email=email).first()
        if capture_model:
            if capture_model.captcha.lower() != captcha.lower():
                raise ValidationError("验证码错误")
        else:
            print("验证码异常")
            raise ValidationError("验证码异常")

    def validate_email(self, field):
        e1 = UserModel.query.filter_by(email=field.data).first()
        if e1:
            print("email is exist")
            raise ValidationError("邮箱已注册")


class LoginForm(FlaskForm):
    email = StringField("email", validators=[InputRequired(), email()])
    password = StringField(validators=[InputRequired(), length(min=6, max=20)])

    def validate_email(self, field):
        e1 = UserModel.query.filter_by(email=field.data).first()
        if not e1:
            print("email is not exist")
            raise ValidationError("邮箱未注册")

    def validate_password(self, pwd):
        email = self.email.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            if not check_password_hash(user_model.password,pwd.data):
                print("user_model.password:",user_model.password)
                raise ValidationError("密码错误")
        session['user_id'] = user_model.id



