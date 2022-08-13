from flask import Blueprint, render_template, request, redirect
from decorator import *
from .forms import QAForm, CommentForm
from models import QuestionModel, CommentModel
from flask import session
from ext import db

bp = Blueprint('qa', __name__, url_prefix='/')


@bp.route('/')
def index():
    questions = QuestionModel.query.all()
    print(questions)
    return render_template('index.html', articles=questions)


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


@bp.route("/question<int:question_id>")
def question(question_id):
    qa = QuestionModel.query.get(question_id)
    print(qa.comments)
    return render_template('question.html', question=qa)


@bp.route("/comment<int:question_id>", methods=['POST'])
def comment(question_id):
    comment_form = CommentForm()
    user_id = session.get('user_id')
    com = CommentModel(content=comment_form.comment.data, author_id=user_id, question_id=question_id)
    db.session.add(com)
    db.session.commit()
    return redirect(url_for('qa.question',question_id=question_id))
