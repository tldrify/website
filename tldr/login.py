from flask import request, redirect, url_for
from flask_login import LoginManager
from tldr.model import db, User
from tldr import app

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return db.session.query(User).get(id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect("%s?next=%s" % (url_for("login"), request.path))
