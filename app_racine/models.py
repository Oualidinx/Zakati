
from app_racine import db,application, login
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class Critere(db.Model):
	id = db.Column(db.String(40) , primary_key = True , nullable = False)
	categorie = db.Column(db.String(50))
	poids = db.Column(db.Float , nullable = False)
	def __str__(self):
		return 'Critere ( {a}, {b})'.format(a = self.id , b = str(self.poids))

class Fournit(db.Model):
	id = db.Column(db.Integer , primary_key = True , nullable=False)
	mosque_id = db.Column(db.Integer, db.ForeignKey('mosque.id'), nullable = False)
	donneur_id = db.Column(db.Integer,db.ForeignKey('donneur.id') ,nullable = False)
	montant = db.Column( db.Float, default = 0.0)
	date = db.Column( db.DateTime, default = datetime.utcnow)

class  situation_garant(db.Model):
	garant_id = db.Column(db.String(10), db.ForeignKey('garant.id') ,primary_key = True, nullable=False)
	critere_id = db.Column(db.String(40), db.ForeignKey('critere.id'), primary_key = True )

class situation_personne(db.Model):
	personne_id = db.Column(db.Integer , db.ForeignKey('personne.id') , primary_key = True)
	critere_id = db.Column(db.String(40), db.ForeignKey('critere.id') , primary_key = True )

class Mosque(db.Model):
	id = db.Column(db.Integer, primary_key = True, nullable = False)
	nom = db.Column(db.String(50), nullable = False)
	inscrits = db.relationship('Garant', backref = 'beneficaire', lazy = 'subquery')
	imam = db.Column(db.String(50) , nullable = False)
	addresse = db.Column(db.String(100), nullable = False)
	state = db.Column(db.String(50), nullable = False)
	country = db.Column(db.String(50), nullable = False, default = "الجزائر")
	num_tele = db.Column(db.String(10), nullable = False)
	#email = db.Column(db.String(100))
	user_account = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	def __repr__(self):
		return "Mosque ('{a}','{b}','{c}','{d}')".format(a = self.id , b = self.nom, c = self.num_tele,d = self.inscrits)
	
	def print_resume(self):
		return printPDF_resume_view()

	def tendance(self):#حساب السهم
		min_points = Garant.query.filter_by(mosque_id=self.id).filter_by(actif=1).order_by(Garant.Solde_points.asc()).first().Solde_points
		g_list = Garant.query.filter_by(mosque_id=self.id).filter_by(actif=1)
		for person in g_list:
			person.Solde_finale = round(person.Solde_points / min_points, 2)
			db.session.add(person)
			db.session.commit()
		
	def get_value(self):#قيمة السهم في المسجد
		g_list = Garant.query.filter_by(mosque_id = self.id)
		somme = 0
		for person in g_list:
			somme += person.Solde_finale
		donnations= Fournit.query.filter_by(mosque_id=self.id)
		sum_dons = 0
		for d in donnations:
			sum_dons += d.montant
		return sum_dons/somme

class Garant(db.Model):
	id = db.Column(db.String(10), primary_key = True, nullable=False) #le compte ccp
	cle_CCP = db.Column(db.Integer , nullable = False)
	nom = db.Column(db.String(50), nullable = False)
	prenom = db.Column(db.String(50), nullable = False)
	date_inscrit = db.Column(db.DateTime , nullable = False, default = datetime.utcnow)
	date_nais = db.Column(db.DateTime , nullable = False)
	num_extrait_nais = db.Column(db.Integer, nullable = False)
	Solde_finale = db.Column(db.Float,default=0)#عدد الاسهــم
	Solde_points = db.Column(db.Integer,default=0)#رصيد النقاط
	Solde_part_financiere = db.Column(db.Float,default=0)#المبلغ المستحق للمحتاج
	actif = db.Column(db.Integer, default = 1)
	familles = db.relationship('Personne' , backref="person", lazy = True)
	mosque_id = db.Column(db.Integer , db.ForeignKey('mosque.id'), nullable = False)
	def __repr__(self):
		return "Garant('{a}' , '{b}', '{c}', {d})".format(a=self.nom , b=str(self.prenom), c = self.date_inscrit, d = str(self.Solde_points))

	def print_form(self):#return a response token
		return printPDF_view(self.id)
	
	def get_total_sum(self):
		self.Solde_part_financiere = self.Solde_finale * Mosque.query.filter_by(id = self.mosque_id).first().get_value()
		db.session.add(self)
		db.session.commit()
		return self.Solde_part_financiere

class Personne(db.Model):
	id = db.Column(db.Integer , primary_key = True , nullable=False)
	nom = db.Column(db.String(50) , nullable = False)
	prenom = db.Column(db.String(50) , nullable = False)
	date_naissance = db.Column(db.DateTime , nullable = False)
	relation_ship = db.Column(db.String(6) , nullable = False, default = "")
	garant_id = db.Column(db.String(10), db.ForeignKey('garant.id'), nullable = False) #le compte ccp
	def __repr__(self):
		return "Personne:{a}{b}{c}{d}".format(a=self.nom,b = self.prenom, c = self.date_naissance, d=self.garant_id )

participe = db.Table(
	'participe',
	db.Column('donneur_id',db.Integer , db.ForeignKey('donneur.id'), primary_key = True,nullable = False),
	db.Column('projet_id', db.Integer, db.ForeignKey('projet.id'), primary_key = True,nullable = False)
)

class Donneur(db.Model):
	id = db.Column(db.Integer , primary_key = True,nullable = False)
	nom = db.Column(db.String(50) , nullable=False)
	prenom = db.Column(db.String(50) , nullable = False)
	adresse = db.Column(db.String(100) , nullable = False)
	num_tele = db.Column(db.String(10), nullable=False)# peut etre changé vers l'email
	user_account = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	
concerner = db.Table(
	'concerner',
	db.Column('garant_id', db.String(10), db.ForeignKey('garant.id'), primary_key = True, nullable=False),
	db.Column('projet_id', db.Integer , db.ForeignKey('projet.id'),primary_key = True , nullable = False)
)

class Projet(db.Model):
	id = db.Column(db.Integer , primary_key = True , nullable = False)
	title =  db.Column(db.String(50), nullable = False)
	Description = db.Column(db.Text)
	montant_estime = db.Column(db.Float, nullable = False, default = 0.0)
	montant_quantise = db.Column(db.Float, default = 0.0)
	def __str__(self):
		return "Projet ('{a}','{title}',{b}','{c}','{d}')".format(
			title = self.title,
			b = self.Description,
			c = str(self.montant_vise),
			d = str(self.montant_quantise)
		)

@login.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
	
class User(db.Model, UserMixin):
	id =  db.Column(db.Integer, primary_key = True, nullable = False )
	username = db.Column(db.String(50), nullable = False)
	password = db.Column(db.String(100), nullable = False)
	def __repr__(self):
		return "User('{a}','{b}')".format(a = str(self.id), b = self.username)
	
	def get_reset_token(self, expires_sec = 1800):
		s = Serializer(application.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id' : self.id}).decode('utf-8')
			
	@staticmethod
	def verify_reset_token(token):
		s = Serializer(application.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)
from app_racine.utils import printPDF_view,printPDF_resume_view