import re
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo
from wtforms import StringField, SubmitField, TextAreaField,DateField
from wtforms import FloatField, PasswordField, IntegerField, SelectField, FieldList
from wtforms import SelectMultipleField, FormField, BooleanField
from .models import Critere, Mosque, Donneur, User, Garant
import arabic_reshaper as reshaper


"""
	formulaire dédiés spécialement au côté administration de la platforme
	D'une part, ces formulaire sert à définir la partie dynamique de toutes les utilisateur de l'application Zakat
	à titre d'exemple: 
		l'ajout des donneurs , des mosques et les critères de classification des garants
	D'autre part, on peut trouver une interfacite interactive afin de visualiser quelques états sorties 
	de l'application comme des statistiques , des listes sur l'etat des mosques, donneurs , projets et 
	critere
"""


class critereForm(FlaskForm):
	"""docstring for critere"""
	categorie = StringField('الحالة التي يتبعها المعيار ', validators=[DataRequired(), Length(max = 50)])
	label = StringField('تسمية المعيـار :', validators=[DataRequired(), Length(min = 4 , max=40)])
	poids = StringField('قيمـة المعيــار :' , validators=[DataRequired()])
	submit= SubmitField("إضــافة")
	def validate_label(self, label):
		critere = Critere.query.filter_by(id = label.data).first()
		if critere :
			raise ValidationError('لقـد تم ادخـال هذا المعيار من قبل')
	
	def validate_poids(self,poids):
		if float(poids.data) <= 0 :
			raise ValidationError('القيمة المعدومة غير مقبولة')

class mosqueForm(FlaskForm):
	nom = StringField("اســـم المسجــد :", validators=[DataRequired()])
	imam = StringField("اسم الإمــام :", validators=[DataRequired(), Length(min= 5 , max= 50)])
	adresse = StringField("العنـــوان :", validators=[DataRequired()])
	#state = SelectField('الولايــــة', validators=[DataRequired()], choices = ['اختر ...','الجزائر','قسنطينة','سطيف','عنابة','وهران','سيدي بلعباس','تلمسان','الشلف','الطارف','سعيدة','الجلفة','الأغواط','تمنراست','بسكرة','ورقلة','غرداية','الوادي','إليزي','تبسة','ام البواقي','خنشلة','برج بو عريريج','المسيلة','البليدة','بجاية','جيجل','تيبازة','تيزي وزو','باتنة','سوق اهراس','سكيكدة','قالمة','ميلة','المدية','البويرة','ادرار','تندوف','البيض','بومرداس','تيارت','غليزان','بشار','عين الدفلى','عين تموشنت','معسكر','مستغانم'])
	state = StringField('الولاية', validators=[DataRequired()])
	#email = StringField("البريد الالكتروني :"), validators=[Email()])
	phone_num = StringField("رقــم الهاتف :", validators=[DataRequired()])
	password = PasswordField("كلمــة المرور :", validators=[DataRequired()])
	confirm_password = PasswordField("تأكيـــد كلمــة المرور :", validators=[DataRequired(), EqualTo('password', message ='كلمتي المرور غير متطابقيتين')])
	submit= SubmitField("إضــافة")
	def validate_phone_num(self, phone_num):
		compte = User.query.filter_by(username  = phone_num.data).first()
		if compte:
			raise ValidationError('مستخدم موجود من قبل')

	def validate_nom(self, nom):
		if re.search('[0-9]', nom.data):
			raise ValidationError('لا يوجد أي رقم في اسم المسجد')

	def validate_imam(self, imam):
		if re.search('[0-9]', imam.data):
			raise ValidationError('لا يوجد أي رقم في اسم و لقب')

class donneurForm(FlaskForm):
	nom = StringField("اللقـــب :", validators = [DataRequired()])
	prenom = StringField("الاســـم :", validators = [DataRequired()])
	adresse = StringField("العنوان :", validators = [DataRequired()])
	num_tele = StringField("رقـم الهاتف :", validators = [DataRequired()])
	password = PasswordField("كلمــة المرور :", validators=[DataRequired()])
	confirm_password = PasswordField("تأكيـــد كلمــة المرور :", validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField("إضــافة")
	def validate_num_tele(self , num_tele):
		compte = User.query.filter_by(username = num_tele.data).first()
		if compte:
			raise ValidationError("رقـم الهاتف موجود مسبقا, الرجاء التأكـد من الرقم مجددا")

	def validate_nom(self, nom):
		if re.search('[0-9]', nom.data):
			raise ValidationError('لا يوجد أي رقم في اللقب')

	def validate_prenom(self, nom):
		if re.search('[0-9]', nom.data):
			raise ValidationError('لا يوجد أي رقم في اللقب')

class LoginForms(FlaskForm):
	"""docstring for LoginForms"""
	username = StringField('اسم المستخـدم :' , validators=[DataRequired()])
	password = PasswordField('كلمة المرور :', validators=[DataRequired()])
	submit = SubmitField('الدخـول')
	def validate_username(self, username):
		t_user = User.query.filter_by(username = username.data).first()
		if t_user is None:
			raise ValidationError('لا يوجد أي حساب بهذا الاسم الرجاء التسجيل')

class RequestResetForm(FlaskForm):
	"""docstring for RequestResetForm"""
	username = StringField('اسم المستخدم او رقم الهاتف', validators=[DataRequired()])
	submit = SubmitField('طلب استعادة كلمة المرور')
	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()
		if user is None:
			raise ValidationError('لا يوجد أي حساب بهذا الاسم الرجاء التسجيل')

class TokenForm(FlaskForm):
	token = IntegerField('الـرمـز', validators=[DataRequired()])
	submit = SubmitField('التحقق من الرمز')

class ResetPasswordForm(FlaskForm):
	"""docstring for ResetPasswordForm"""
	password = PasswordField('كلمة المرور الجديدة', validators=[DataRequired()])
	confirm_password = PasswordField('تأكيد كلمة المرور', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('حفظ')

class ProjectsForm(FlaskForm):
	"""docstring for ProjectsForm"""
	title = StringField('عنوان المشــــروع', validators=[DataRequired(), Length(max = 50)])
	Description= TextAreaField('تعريف المشروع', validators=[DataRequired(), Length(max = 1500)])
	montant_estime = FloatField('القيمة المقدرة', validators=[DataRequired()])
	submit = SubmitField('أضـــف')
	def validate_title(self, title):
		if title.data == '':
			raise ValidationError('حقل مطلوب، يجب كتابـــة العنوان')
	
"""
	formulaires pour le côté des mosque comme : 
		l'ajout d'une nouvelles famille
		mise à jour des informations concernant la mosque elle meme 
"""

class personnes_par_garant(FlaskForm):
	p_nom = StringField("اللقــــب", validators=[DataRequired(), Length(max = 50)])
	p_prenom = StringField("الاســـم", validators=[DataRequired(), Length(max = 50)])
	p_date_nais = DateField("تاريــخ الميلاد", validators=[DataRequired()], format= '%d/%m/%Y')
	education = BooleanField('التمـدرس')
	handicap = BooleanField('الاعـاقـة')
	malade_cronic = BooleanField('المرض المزمن')
	p_relation_ship = SelectField("صلة القرابــة ",validators=[DataRequired()], choices=[("","اختـــر"),("ابن(ة)","ابن(ة)"), ("زوجة","زوجة"),("الأب","الأب"),("الأم","الأم"),("الجد","الجد"),("الجدة","الجدة")])
	#submit = SubmitField("أضف فردا آخر")

class RegisterGarantForm(FlaskForm):
    nom = StringField("اللقــــب :", validators=[DataRequired(), Length(min = 4, max=50)])
    prenom = StringField("الإســـم :", validators=[DataRequired(), Length(min= 4 , max=50)])
    date_nais = DateField ("تاريــخ الميلاد :", validators=[DataRequired()], format='%d/%m/%Y')
    compte_ccp = StringField("الحســـاب البريدي :", validators=[DataRequired() , Length(max=12)])
    cle_ccp = StringField("المفتــاح :", validators=[DataRequired()])
    num_extrait_nais = StringField("رقـم شهادة الميلاد :", validators=[DataRequired()])
    situation_sante = SelectMultipleField("الحالــة الصحية :", choices=[(objet.id,objet.id) for objet in Critere.query.filter_by(categorie = "الصحية")])
    situation_sociale = SelectMultipleField("الحالــة الاجتمـــاعيـة :", choices=[(objet.id,objet.id) for objet in Critere.query.filter_by(categorie = "الاجتماعية")])
    situation_familliale = SelectMultipleField("الحالــة العائليــــــة :", choices=[(objet.id,objet.id) for objet in Critere.query.filter_by(categorie = "العائلية")])
    famille = []
    submit = SubmitField("أضــــف")
    def validate_compte_ccp(self, compte_ccp):
        if Garant.query.filter_by(id = compte_ccp.data).first():
            raise ValidationError("خطـأ في كتابة الحساب البريدي")

class update_account_form(FlaskForm):
    """docstring for update_account_form"""
    nom_imam = StringField("اسـم  الامـام :", validators=[DataRequired() , Length(min = 10 , max = 50)])
    num_tele = StringField("رقـم الهاتــف :", validators=[DataRequired(), Length(max = 10)])
    submit = SubmitField("تعـديل العملية")

class register_new_donnation(FlaskForm):
    """docstring for register_new_donnation"""
    #donneur = SelectField("المحســـن :", choices = [(objet.id , objet.id) for objet in Donneur.query.all()],validators=[DataRequired()])
    donneur = StringField("المحســـن :", validators=[DataRequired()])
    montant = StringField("قيمة التبرع :", validators=[DataRequired()])
    submit = SubmitField("تأكيــــد")
    def validate_montant(self, montant):
    	if int(montant.data) <= 0:
    		raise ValidationError("قيمــــة خاطئــــة")

class parameter_utils_form(FlaskForm):
	taux_scolaire = StringField("قيمة المنحة للفرد الواحد", validators=[DataRequired()])
	taux_prime_m = StringField("قيمة المبلغ للفرد (خاص بالمنحة الشهرية)",validators=[DataRequired()])
	salaire_base = StringField("قيمة المبلغ للفرد (الأجر القاعدي)",validators=[DataRequired()])
	submit = SubmitField("ارســــــال")
	def validate_taux_scolaire(self, taux_scolaire):
		if int(taux_scolaire.data) <= 0:
			raise ValidationError('الرجــاء تعريف  القيمة بطريقة صحيحة')
	
	def validate_taux_prime_m(self, taux_prime_m):
		if int(taux_prime_m.data) <= 0:
			raise ValidationError('الرجــاء تعريف  القيمة بطريقة صحيحة')
	
	def validate_salaire_base(self, salaire_base):
		if int(salaire_base.data) <= 0:
			raise ValidationError('الرجــاء تعريف  القيمة بطريقة صحيحة')
	
	