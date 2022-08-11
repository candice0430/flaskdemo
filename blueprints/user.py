from flask import Blueprint, render_template, request, redirect, url_for, jsonify,flash
from flask_mail import Message

from ext import mail, db,csrf
from utils import utils
from models import EmailCapatureModel, UserModel
import datetime
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        login_form = LoginForm(request.form)
        if login_form.validate():
            print("验证通过")
            return redirect("/")
        else:
            print("验证失败", login_form.errors)
            flash("邮箱或密码不正确")
            return redirect(url_for("user.login"))


@bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        reg_form = RegisterForm(request.form)
        if reg_form.validate():
            username = reg_form.username.data
            password = reg_form.password.data
            email = reg_form.email.data
            user = UserModel(email=email, password=generate_password_hash(password), username=username)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.login"))
        else:
            return redirect(url_for("user.register"))
        return jsonify(reg_form.errors)


@bp.route('/mail', methods=["POST"])
@csrf.exempt
def my_mail():
    captcha = utils.gen_captcha()
    print("captcha:", captcha)
    reg_form = RegisterForm(request.form)
    email = request.form.get("email")
    print("email:", email)
    if email:
        msg = Message(subject='Hello', recipients=[email])
        msg.body = f"hi,您的验证码是：{captcha} ,请不要告诉任何人！"
        mail.send(msg)

        capture_model = EmailCapatureModel.query.filter_by(email=email).first()
        print("capture_model:",capture_model)
        if capture_model:
            capture_model.captcha = captcha
            capture_model.create_time = datetime.datetime.now()
            db.session.commit()
        else:
            capture_model = EmailCapatureModel(email=email, captcha=captcha)
            db.session.add(capture_model)
            db.session.commit()
        print("send captcha:", captcha)
        return jsonify({"code": 200, "msg": "验证码发送成功"})
    else:
        return jsonify({"code": 400, "msg": "请输入邮箱"})
