from flask import Blueprint,render_template,request,redirect,url_for
from flask_mail import Message
from ext import mail,db
from utils import utils
from models import EmailCapatureModel
import datetime
from .forms import RegisterForm


bp = Blueprint('user',__name__,url_prefix='/user')


@bp.route('/login')
def login():
    return render_template("login.html")


@bp.route('/register',methods=["GET","POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        print(request.args)
        reg_form = RegisterForm(request.form)
        print(reg_form.username)
        print(reg_form.email)
        print(reg_form.pwd)
        print(reg_form.capture)
        if reg_form.validate():
            print("validate is ok")
            redirect(url_for("user.login"))
        else:
            print("fail===========")
            redirect(url_for("user.register"))
        return "success"

@bp.route('/mail')
def my_mail():
    capture = utils.gen_capture()
    # db.session
    email = request.args.get('email')
    print("email:",email)
    if email:
        msg = Message(subject='Hello', recipients=['378340642@qq.com'])
        msg.body = f"hi,您的验证码是：{capture} ,请不要告诉任何人！"
        mail.send(msg)

        capture_model = EmailCapatureModel.query.filter_by(email=email).first()
        if capture_model:
            capture_model.capture = capture
            capture_model.create_time = datetime.datetime.now()
            db.session.commit()
        else:
            capture_model = EmailCapatureModel(email=email, capture=capture)
            db.session.add(capture_model)
            db.session.commit()
        return 'success'
    else:
        return "请输入邮箱！"

