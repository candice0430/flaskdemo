from flask import g,redirect,url_for
from functools import wraps


def login_required(func):
    print("he===================")

    @wraps(func)
    def wrapper():
        print("comein_-------decorator.....")
        if hasattr(g, "user"):
            return func()
        else:
            return redirect(url_for('user.login'))

    return wrapper
