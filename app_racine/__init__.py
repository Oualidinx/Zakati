#!../venv/bin/python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy

from flask import Flask
from flask_login import LoginManager
import arabic_reshaper as reshaper

from apifairy import APIFairy
from flask_marshmallow import Marshmallow

from config import config

app = Flask(__name__)

database = SQLAlchemy()

login = LoginManager(app)

api_fairy = APIFairy()

marsh = Marshmallow()


def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app()

    login.login_view = 'auth_bp.login'
    login.login_message_category = "info"
    login.login_message = reshaper.reshape(u"هـذه الخدمة تتطلب تسجيل الدخول")

    from app_racine.master import master_bp as master_bp

    app.register_blueprint(master_bp)

    from app_racine.authentication import auth_bp as a_bp

    app.register_blueprint(a_bp)

    from app_racine.mosque import mosque_bp as m_bp

    app.register_blueprint(m_bp)

    from app_racine.users import user_bp as user_bp

    app.register_blueprint(user_bp)

    marsh.init_app(app)
    database.init_app(app)
    return app
