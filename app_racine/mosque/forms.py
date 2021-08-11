import re

from flask_login import current_user
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms.fields.html5 import DateField
from wtforms import StringField, IntegerField, FloatField, SubmitField, SelectField, BooleanField, \
    SelectMultipleField, PasswordField
from wtforms.validators import Length, DataRequired, ValidationError, EqualTo
from app_racine.users.models import User
from app_racine.mosque.models import *
import re

phone_number_regex = re.compile('^[\+]?[(]?[0-9]{2}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,7}$')


class EditPasswordForm(FlaskForm):
    current_password = PasswordField('كلمة المرور الحالية* :', validators=[DataRequired()])
    password = PasswordField("كلمــة المرور :*", validators=[DataRequired()])
    confirm_password = PasswordField("تأكيـــد كلمــة المرور :*",
                                     validators=[DataRequired(),
                                                 EqualTo('password', message='كلمتي المرور غير متطابقتين')])
    submit = SubmitField('تعديل')

    def validate_current_password(self, current_password):
        user = User.query.get(current_user.id)
        if not check_password_hash(user.password, current_password.data):
            raise ValidationError('كلمة المرور خاطئة')


class UpdateAccountForm(FlaskForm):
    email = StringField("البريد الالكتروني :")
    phone_num = StringField("رقــم الهاتف(الخاص بالامام) :*", validators=[DataRequired()])
    first_name = StringField('اسم الامام :*', validators=[DataRequired()])
    last_name = StringField('لقب الامام :*', validators=[DataRequired()])
    username = StringField('اسم المستخدم :')
    current_password = PasswordField('كلمة المرور الحالية* :', validators=[DataRequired()])
    submit = SubmitField("تعديــل")

    def validate_current_password(self, current_password):
        user = User.query.get(current_user.id)
        if not check_password_hash(user.password, current_password.data):
            raise ValidationError('كلمة المرور خاطئة')

    def validate_phone_num(self, phone_num):
        if phone_number_regex.search(phone_num.data) is None:
            raise ValidationError('خطا في كتابة رقم الهاتف')


class PersonPerGarant(FlaskForm):
    p_nom = StringField("اللقــــب", validators=[Length(max=50)])
    p_prenom = StringField("الاســـم", validators=[Length(max=50)])
    p_date_nais = DateField("تاريــخ الميلاد", default=datetime.utcnow().date())
    education = BooleanField('التمـدرس')
    handicap = BooleanField('الاعـاقـة')
    malade_cronic = BooleanField('المرض المزمن')
    p_relation_ship = SelectField("صلة القرابــة ",
                                  choices=[("", "اختـــر"), ("ابن(ة)", "ابن(ة)"), ("زوجة", "زوجة"), ("الأب", "الأب"),
                                           ("الأم", "الأم"), ("الجد", "الجد"), ("الجدة", "الجدة")])


class RegisterGarantForm(FlaskForm):
    nom = StringField("اللقــــب :", validators=[DataRequired(), Length(min=4, max=50)])
    prenom = StringField("الإســـم :", validators=[DataRequired(), Length(min=4, max=50)])
    date_nais = DateField("تاريــخ الميلاد :", validators=[DataRequired()], default=datetime.utcnow().date())
    address = StringField('العنـوان: ', validators=[DataRequired()])
    phone_number = StringField('رقم الهاتف: ', validators=[DataRequired()])
    compte_ccp = StringField("الحســـاب البريدي :", validators=[DataRequired(), Length(max=12)])
    cle_ccp = IntegerField("المفتــاح :", validators=[DataRequired()])
    num_extrait_nais = StringField("رقـم شهادة الميلاد :", validators=[DataRequired()])
    situation_sante = SelectMultipleField("الحالــة الصحية :", coerce=int, validate_choice=False)
    situation_sociale = SelectMultipleField("الحالــة الاجتمـــاعيـة :", coerce=int, validate_choice=False)
    situation_familliale = SelectMultipleField("الحالــة العائليــــــة :", coerce=int, validate_choice=False)
    submit = SubmitField("أضــــف")

    def validate_compte_ccp(self, compte_ccp):
        if Garant.query.filter_by(ccp=compte_ccp.data).first():
            raise ValidationError("الحساب البريدي موجود من قبل")

    def validate_num_extrait_nais(self, num_extrait_nais):
        if Garant.query.filter_by(num_extrait_nais=num_extrait_nais.data).first():
            raise ValidationError("رقم شهادة الميلاد موجود من قبل")

    def validate_phone_number(self, phone_number):
        if phone_number_regex.search(phone_number.data) is None:
            raise ValidationError("خطأ في كتابة رقم الهاتف")
        if Garant.query.filter_by(phone_number=phone_number.data).first():
            raise ValidationError("رقم الهاتف موجود من قبل")

    def validate_situation_sante(self, situation_sante):
        pass

    def validate_situation_sociale(self, situation_sociale):
        pass

    def validate_situation_familliale(self, situation_familliale):
        pass

    def validate_nom(self, nom):
        garant = Garant.query.filter_by(nom=nom.data) \
            .filter_by(prenom=self.prenom.data) \
            .filter_by(date_nais=datetime.strftime(self.date_nais.data, "%Y-%m-%d")) \
            .filter_by(address=self.address.data) \
            .first()
        if garant:
            raise ValidationError('هذا الكفيل مسجل من قبل')

    def validate_prenom(self, prenom):
        person = Personne.query.filter_by(nom=self.nom.data) \
            .filter_by(prenom=prenom.data) \
            .filter_by(date_naissance=datetime.strftime(self.date_nais.data, "%Y-%m-%d")) \
            .first()
        if person:
            raise ValidationError('هذا الكفيل قد تم تسجيله كفرد مكفول لدى كفيل آخر')


class RegisterNewDonationForm(FlaskForm):
    """docstring for register_new_donation"""
    project = SelectField("المشـروع :", validate_choice=False)
    first_name = StringField("اسم المحســـن :", validators=[DataRequired()])
    last_name = StringField("لقب المحســـن :", validators=[DataRequired()])
    phone_number = StringField('رقم الهاتف:', validators=[DataRequired()])
    montant = FloatField("قيمة التبرع :", validators=[DataRequired()])
    submit = SubmitField("تأكيــــد")

    def validate_phone_number(self, phone_number):
        if phone_number_regex.search(phone_number.data) is None:
            raise ValidationError("خطأ في كتابة رقم الهاتف")

    def validate_montant(self, montant):
        if int(montant.data) <= 0:
            raise ValidationError("قيمــــة خاطئــــة")


class ReceiptAmountForm(FlaskForm):
    mosque = SelectField('استلام من طرفة', validate_choice=False)
    amount = FloatField('المبلــغ', validators=[DataRequired()])
    pass


class ProjectsSelectForm(FlaskForm):
    projects = SelectField('المحتاجين حسب المشروع: ', validate_choice=False)
