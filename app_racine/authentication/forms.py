from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from app_racine.users.models import *


class LoginForms(FlaskForm):
    """docstring for LoginForms"""
    username = StringField('اسم المستخـدم :', validators=[DataRequired()])
    password = PasswordField('كلمة المرور :', validators=[DataRequired()])
    submit = SubmitField('الدخـول')

    def validate_username(self, username):
        t_user = User.query.filter_by(username=username.data).first()
        if t_user is None:
            raise ValidationError('لا يوجد أي حساب بهذا الاسم الرجاء التسجيل')


class RequestResetForm(FlaskForm):
    """docstring for RequestResetForm"""
    username = StringField('رقم الهاتف', validators=[DataRequired()])
    submit = SubmitField('طلب استعادة كلمة المرور')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('لا يوجد أي حساب بهذا الاسم الرجاء التسجيل')


class TokenForm(FlaskForm):
    token = StringField('الـرمـز', validators=[DataRequired()])
    submit = SubmitField('التحقق من الرمز')



class ResetPasswordForm(FlaskForm):
    """docstring for ResetPasswordForm"""
    password = PasswordField('كلمة المرور الجديدة', validators=[DataRequired()])
    confirm_password = PasswordField('تأكيد كلمة المرور', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('حفظ')
