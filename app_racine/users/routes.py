from app_racine.users import user_bp
from flask import session, redirect, url_for, render_template
from app_racine.authentication import auth_bp


@user_bp.route('/')
def index():
    return render_template('site/index.html')