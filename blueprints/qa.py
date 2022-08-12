from flask import Blueprint, render_template
from decorator import *

bp = Blueprint('qa', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template('index.html')



@bp.route('/public_qa')
@login_required
def public_qa():
    return render_template('public_question.html')
