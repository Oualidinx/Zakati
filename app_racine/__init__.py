#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login.login_manager import LoginManager
import arabic_reshaper as reshaper
from flask_bcrypt import Bcrypt

application = Flask(__name__)
db_parameters={
    'driver' : 'mysql',
    'user' : 'oualid',
    'password': '',
    'host':'localhost',
    'db_name':'mydb',
    'charset' :'utf8'
}
application.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


application.config['SQLALCHEMY_DATABASE_URI'] = "{driver}://{user}:{password}@{host}/{db_name}?charset={charset}".format(**db_parameters)

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(application)
bcrypt = Bcrypt(application)
login = LoginManager(app = application)

login.login_view = 'login'
login.login_message_category = "info"
login.login_message = reshaper.reshape(u"هـذه الخدمة تتطلب تسجيل الدخول")
from app_racine import routes
