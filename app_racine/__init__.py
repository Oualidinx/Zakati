#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login.login_manager import LoginManager
import arabic_reshaper as reshaper
from flask_bcrypt import Bcrypt

app = Flask(__name__)
db_parameters={
    'driver' : 'postgres',
    'port': 5432,
    'user' : 'xvxgsgmdbdjrsr',
    'password': '598bbf294f2af3860f052210a5b9cfa78e2890a81d1d94955824ccc23c49bfe6',
    'host':'ec2-34-202-65-210.compute-1.amazonaws.com',
    'db_name':'d7i4nsjusks75a'
}
app.config['SQLALCHEMY_DATABASE_URI'] = "{driver}://{user}:{password}@{host}:{port}/{db_name}".format(**db_parameters)

"""
db_parameters={
    'driver' : 'mysql',
    'user' : 'oualid',
    'password': '',
    'host':'localhost',
    'db_name':'database'
}
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245' 
app.config['SQLALCHEMY_DATABASE_URI'] = "{driver}://{user}:{password}@{host}/{db_name}".format(**db_parameters)
"""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login = LoginManager(app = app)

login.login_view = 'login'
login.login_message_category = "info"
login.login_message = reshaper.reshape(u"هـذه الخدمة تتطلب تسجيل الدخول")
