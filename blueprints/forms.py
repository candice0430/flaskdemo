from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length,InputRequired,equal_to,email,DataRequired
from ext import db


class RegisterForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(),Length(min=6,max=20)])
    email = StringField("email", validators=[DataRequired(),email()])
    pwd = StringField("password", validators=[DataRequired(),Length(min=6,max=20)])
    confirm_pwd = StringField("password_confirm", validators=[DataRequired(),equal_to(pwd)])
    capture = StringField("captcha", validators=[DataRequired(),Length(min=4,max=4)])

    def validate_capture(self):
        print("dddddd")

    def validate_email(self):
        print("dddddd11111")
        e1 = db.query.filter(email=self.email).first()
        if e1:
            raise "邮箱已注册"


