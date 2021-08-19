import re

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms.validators import Length, DataRequired, ValidationError, EqualTo

from app_racine.master.models import *
from app_racine.users.models import *
from app_racine.mosque.models import *


class CritereForm(FlaskForm):
    categorie = SelectField('الحالة التي يتبعها المعيار ', validate_choice=False)
    label = StringField('تسمية المعيـار :', validators=[DataRequired(), Length(min=4, max=40)])
    poids = FloatField('قيمـة المعيــار :', validators=[DataRequired()])
    submit = SubmitField("إضــافة")

    def validate_label(self, label):
        critere = Critere.query.filter_by(label=label.data).filter_by(category=self.categorie.data).first()
        if critere:
            raise ValidationError('لقـد تم ادخـال هذا المعيار من قبل')

    def validate_poids(self, poids):
        if poids.data <= 0:
            raise ValidationError('القيمة المعدومة غير مقبولة')

    def validate_categorie(self, categorie):
        if categorie.data == 'None':
            raise ValidationError('يرجى اختيار الحالة التي يتبعها هذا المعيار')


class EditCritereForm(CritereForm):
    submit = SubmitField('تعديل')

    def validate_label(self, label):
        pass


class ProjectsForm(FlaskForm):
    """docstring for ProjectsForm"""
    title = StringField('عنوان المشــــروع', validators=[DataRequired(), Length(max=50)])
    Description = TextAreaField('تعريف المشروع', validators=[DataRequired(), Length(max=1500)])
    montant_estime = FloatField('القيمة المقدرة', validators=[DataRequired()])
    submit = SubmitField('أضـــف')

    def validate_title(self, title):
        if title.data == '':
            raise ValidationError('حقل مطلوب، يجب كتابـــة العنوان')


class EditProjectForm(ProjectsForm):
    submit = SubmitField('تعديل')


class MosqueForm(FlaskForm):
    nom = StringField("الاســـم  :*", validators=[DataRequired()])
    categorie = SelectField("الصـنـف :", choices=[('مسجد', 'مسجد'), ('جمعية', 'جمعية')])
    adresse = StringField("العنـــوان :*", validators=[DataRequired()])
    state = SelectField('الولاية:*', validate_choice=False)
    email = StringField("البريد الالكتروني :")
    phone_num = StringField("رقــم الهاتف :*", validators=[DataRequired()])
    password = PasswordField("كلمــة المرور :*", validators=[DataRequired()])
    confirm_password = PasswordField("تأكيـــد كلمــة المرور :*",
                                     validators=[DataRequired(),
                                                 EqualTo('password', message='كلمتي المرور غير متطابقتين')])
    first_name = StringField('اسم الامام :*', validators=[DataRequired()])
    last_name = StringField('لقب الامام :*', validators=[DataRequired()])
    phone_num_imam = StringField('رقم الهاتف: *', validators=[DataRequired()])
    username = StringField('اسم المستخدم :')
    submit = SubmitField("إضــافة")

    def validate_phone_num(self, phone_num):
        compte = User.query.filter_by(phone_number=phone_num.data).first()
        if compte:
            raise ValidationError('مستخدم موجود من قبل')

    def validate_nom(self, nom):
        mosque = Mosque.query.filter_by(nom=nom.data).filter_by(category=self.categorie.data).first()
        if mosque:
            raise ValidationError('الاسـم موجود من قبل')
        if re.search('[0-9]', nom.data):
            raise ValidationError('لا يوجد أي رقم في اسم المسجد')

    def validate_imam(self, imam):
        if re.search('[0-9]', imam.data):
            raise ValidationError('لا يوجد أي رقم في اسم و لقب')

    def validate_phone_num_imam(self, phone_num_imam):
        user = User.query.filter_by(phone_number=phone_num_imam.data).first()
        if user:
            raise ValidationError('هذا الرقم موجود من قبل')

    def validate_state(self, state):
        if state.data == 'None':
            raise ValidationError('يرجى اختيار الولاية')


class ParameterForm(FlaskForm):
    taux_scolaire = FloatField("(خاص بمنحة التمدرس) قيمة المنحة للفرد الواحد", validators=[DataRequired()])
    taux_prime_m = FloatField("قيمة المبلغ للفرد (خاص بالمنحة الشهرية)", validators=[DataRequired()])
    salaire_base = FloatField("الأجـــر القـاعدي", validators=[DataRequired()])
    submit = SubmitField("ارســــــال")

    def validate_taux_scolaire(self, taux_scolaire):
        if taux_scolaire.data <= 0:
            raise ValidationError('الرجــاء تعريف  القيمة بطريقة صحيحة')

    def validate_taux_prime_m(self, taux_prime_m):
        if taux_prime_m.data <= 0:
            raise ValidationError('الرجــاء تعريف  القيمة بطريقة صحيحة')

    def validate_salaire_base(self, salaire_base):
        if salaire_base.data <= 0:
            raise ValidationError('الرجــاء تعريف  القيمة بطريقة صحيحة')
