from flask import current_app, session, url_for, redirect, flash, request, render_template, abort
from werkzeug.security import check_password_hash
from flask_login import current_user, login_user, logout_user

from app_racine.authentication import auth_bp
from app_racine.authentication.forms import *
from app_racine.users.models import User
from app_racine.mosque.models import Mosque
from app_racine import login


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        if current_user.role == "imam":
            return redirect(url_for('mosque_bp.mosque_dashboard'))
        elif current_user.role == "administrator":
            return redirect(url_for('master_bp.admin_dashboard'))
        elif current_user.role == "donor":
            return redirect(url_for('master_bp.dashboard'))
    form = LoginForms()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=False)
            session["user_id"] = user.id
            next_page = request.args.get('next')
            t_mosque = Mosque.query.filter_by(user_account=user.id).first()

            if t_mosque and user.role == "imam":
                print(t_mosque.to_dict())
                return redirect(next_page) if next_page else redirect(
                    url_for('mosque_bp.mosque_dashboard'))
            elif user.role == "donor":
                return redirect(next_page) if next_page else redirect(url_for('donor_bp.donor_dashboard'))
            elif user.role == "administrator":
                return redirect(next_page) if next_page else redirect(url_for('master_bp.admin_dashboard'))
            else:
                abort(403)
        else:
            flash('خطأ في المعلومات يرجى التأكد و إعادة المحاولة', 'danger')
    return render_template('authentication/login.html', title="زكاة : تسجيل الدخول", form=form)


@auth_bp.route("/logout")
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("auth_bp.login"))
