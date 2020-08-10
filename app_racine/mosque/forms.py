from wtforms import StringField, DateField, SelectMultipleField, SubmitField, SelectField, FloatField, FormField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, ValidationError
from app_racine.models import Garant, Critere, Donneur
import arabic_reshaper as reshaper
import re

class personnes_par_garant(FlaskForm):
    """docstring for personnes_par_garant"""
    nom = StringField("اللقــــب", validatos=[DataRequired(), Length(min=5, max = 50)])
    prenom = StringField("الاســـم", validatos=[DataRequired(), Length(min=5, max = 50)])
    date_nais = DateField("تاريــخ الميلاد", validators=[DataRequired()], format= '%d/%m/%Y')
    relation_ship = SelectField("صلة القرابــة ", choices=["ابن(ة)", "زوجة"])

class RegisterGarantForm(FlaskForm):
    nom = StringField("اللقــــب :", validatos=[DataRequired(), Length(min = 4,   max=50)])
    prenom = StringField("الإســـم :", validatos=[DataRequired(), Length(min= 4 , max=50)])
    date_nais = DateField ("تاريــخ الميلاد :", validators=[DataRequired()], format='%d/%m/%Y')
    compte_ccp = StringField("الحســـاب البريدي :", validators=[DataRequired() , Length(min = 10, max=10)])
    cle_ccp = StringField("المفتــاح :", validatos=[DataRequired()])
    num_extrait_nais = StringField("رقـم شهادة الميلد :", validators=[DataRequired()])
    situation_sante = SelectMultipleField("الحالــة الصحية :", choices=[objet.id for objet in Critere.query.filter_by(categorie = "حالة صحية")])
    situation_sociale = SelectMultipleField("الحالــة الاجتمـــاعيـة :", choices=[objet.id for objet in Critere.query.filter_by(categorie = "حالة اجتماعية")])
    familles = FormField(personnes_par_garant)
    submit = SubmitField("أضــــف")
    def validate_ccp(self, ccp):
        if Garant.query.filter_by(id = ccp.data).first():
            raise ValidationError("هذا الحساب الجاي موجود مسبقا. الشخص المطلوب اما مسجل في مسجد آخر أو الحساب الجاري قد سجلت به عائلة أخرى")
        elif re.search("[A-Z|a-z]" , ccp.data):
            raise ValidationError("خطـأ في كتاة الحساب البريدي")
        
    def validate_cle_ccp(self, cle_ccp):
        if int(cle_ccp.data) <= 0 or re.search("[A-Z|a-z]" , cle_ccp.data) is not None:
            raise ValidationError("معلومة خاطئة")

"""class ResetPasswordForm(FlaskForm):
    #docstring for RequestPasswordForm
    password = PasswordField('كلمة المرور :', validators=[DataRequired()])
    confirm_password = PasswordField('تأكيــد كلمة المرور :', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('تأكيــد العملية')"""

class update_account_form(FlaskForm):
    """docstring for update_account_form"""
    nom_imam = StringField("اسـم  الامـام :", validators=[DataRequired() , Length(min = 10 , max = 50)])
    num_tele = StringField("رقـم الهاتــف :", validators=[DataRequired()], Length(max = 10))
    submit = SubmitField("تعـديل")

class register_new_donnation(FlaskForm):
    """docstring for register_new_donnation"""
    donneur = SelectField("المحســـن :", choices = [(objet.nom , objet.prenom) for objet in Donneur.query.all()],validators=[DataRequired()])
    valeurs_don = FloatField("قيمة التبرع :", validators=[DataRequired()])
    submit = SubmitField("تأكيــــد")
    def validate_valeurs_don(self, valeur):
        if valeur.data <= 0:
            raise ValidationError("قيمــــة خاطئــــة")

class LoginForm(FlaskForm):
    username = StringField("اسم المستخدم :", validators=[DataRequired()])
    password = PasswordField("كلمـة المرور :", validators = [DataRequired()])
    submit = SubmitField("دخــول")