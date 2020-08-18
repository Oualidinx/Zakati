#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login.login_manager import LoginManager
import arabic_reshaper as reshaper
from flask_bcrypt import Bcrypt

app = Flask(__name__)
db_parameters={
    'driver' : 'mysql',
    'user' : 'ynohxpjmaejjnz',
    'password': '8b77a9c380c0c34308924eb8aa07a480d6fef9be579314ea5900b8ee95c4ef9a',
    'host':'ec2-54-91-178-234.compute-1.amazonaws.com',
    'db_name':'database',
    'charset' :'utf8'
}
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://ynohxpjmaejjnz:8b77a9c380c0c34308924eb8aa07a480d6fef9be579314ea5900b8ee95c4ef9a@ec2-54-91-178-234.compute-1.amazonaws.com:5432/d2h6pid7rn64nd" #"{driver}://{user}:{password}@{host}/{db_name}?charset={charset}".format(**db_parameters)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login = LoginManager(app = app)

login.login_view = 'login'
login.login_message_category = "info"
login.login_message = reshaper.reshape(u"هـذه الخدمة تتطلب تسجيل الدخول")
#from app_racine import routes
