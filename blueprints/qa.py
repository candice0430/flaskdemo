from flask import Blueprint, render_template, request,redirect
from decorator import *
from .forms import QAForm
from models import QuestionModel, UserModel
from flask import session
from ext import db

bp = Blueprint('qa', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/public_qa', methods=['GET', 'POST'])
@login_required
def public_qa():
    if request.method == 'GET':
        return render_template('public_question.html')
    else:
        qa_form = QAForm(request.form)
        if qa_form.validate():
            title = qa_form.title.data
            content = qa_form.content.data
            user_id = session.get('user_id')
            question = QuestionModel(title=title, content=content, author_id=user_id)
            db.session.add(question)
            db.session.commit()
            return redirect("/")
        else:
            print(qa_form.errors)
            return render_template('public_question.html')
