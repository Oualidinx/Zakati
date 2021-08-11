from app_racine import db
from datetime import datetime
from app_racine.utilities import PaginationMixin


class Garant(PaginationMixin, db.Model):
    __tablename__ = "garant"
    id = db.Column(db.Integer, primary_key=True, nullable=False)  # le compte ccp
    ccp = db.Column(db.String(20), nullable=False)
    cle_CCP = db.Column(db.Integer, nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_nais = db.Column(db.DateTime, nullable=False)
    num_extrait_nais = db.Column(db.Integer, nullable=False)
    Solde_finale = db.Column(db.Float, default=0)  # عدد الاسهــم
    Solde_points = db.Column(db.Integer, default=0)  # رصيد النقاط
    Solde_part_financiere = db.Column(db.Float, default=0)  # المبلغ المستحق للمحتاج
    is_active = db.Column(db.SmallInteger, default=1)
    familly = db.relationship('Personne', backref="person", lazy=True)
    mosque_id = db.Column(db.Integer, db.ForeignKey('mosque.id'), nullable=False)
    prime_mensuelle = db.Column(db.Float, default=0)
    prime_scolaire = db.Column(db.Float, default=0)
    """def print_form(self):  # return a response token
        return print_PDF_view(self.id)"""

    def print_form(self):  # return a response token
        return PrintPDFView(self.id)

    def get_total_sum(self):
        self.Solde_part_financiere = self.Solde_finale * Mosque.get_value()
        db.session.add(self)
        db.session.commit()
        return self.Solde_part_financiere

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.nom,
            last_name=self.prenom,
            arrows=self.Solde_finale,
            status=self.is_active
        )


class Mosque(PaginationMixin, db.Model):
    __tablename__ = "mosque"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    inscrits = db.relationship('Garant', backref='beneficaire', lazy='subquery')
    addresse = db.Column(db.String(100), nullable=False)

    country = db.Column(db.String(50), nullable=False, default="الجزائر")
    num_tele = db.Column(db.String(10), nullable=False)
    # email = db.Column(db.String(100))
    user_account = db.Column(db.Integer, db.ForeignKey('user.id'))
    category = db.Column(db.String(6), nullable=False)
    state = db.Column(db.Integer, db.ForeignKey('wilaya.id'))
    username = db.relationship('User', primaryjoin="User.id == foreign(Mosque.user_account)", viewonly=True)
    donors = db.relationship('DonateMosque', backref="collected_amount", lazy="subquery")

    def PrintResume(self, project_id):
        return PrintPDFResumeView(project_id)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.nom,
            address=self.addresse,
            category=self.category,
            username=self.username.username
        )

    @staticmethod
    def tendance():
        min_points = 0
        if Garant.query.first():
            min_points = Garant.query.filter_by(is_active=1).order_by(Garant.Solde_points.asc()).first().Solde_points
        if min_points != 0:
            g_list = Garant.query.filter_by(is_active=1).all()
            for person in g_list:
                person.Solde_finale = round(person.Solde_points / min_points, 2)
                db.session.add(person)
                db.session.commit()

    @staticmethod
    def get_value():
        g_list = Garant.query.filter_by(is_active=1).all()
        somme_points = 0
        for person in g_list:
            somme_points += person.Solde_finale
        donations = [sum([donates.amount for donates in mosque.donors]) for mosque in Mosque.query.all() if
                     mosque.donors]
        sum_dons = 0
        for d in donations:
            sum_dons += d
        return sum_dons / somme_points if somme_points > 0 else 0


class SituationGarant(PaginationMixin, db.Model):
    __tablename__ = "situation_garant"
    garant_id = db.Column(db.String(10), db.ForeignKey('garant.id'), primary_key=True, nullable=False)
    critere_id = db.Column(db.String(40), db.ForeignKey('critere.id'), primary_key=True)


class SituationPerson(PaginationMixin, db.Model):
    __tablename__ = "situation_person"
    personne_id = db.Column(db.Integer, db.ForeignKey('personne.id'), primary_key=True)
    critere_id = db.Column(db.String(40), db.ForeignKey('critere.id'), primary_key=True)


class Personne(PaginationMixin, db.Model):
    __tablename__ = "personne"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    date_naissance = db.Column(db.DateTime, nullable=False)
    relation_ship = db.Column(db.String(6), nullable=False, default="")
    garant_id = db.Column(db.String(10), db.ForeignKey('garant.id'), nullable=False)  # le compte ccp


class GarantProject(PaginationMixin, db.Model):
    garant_id = db.Column(db.Integer, db.ForeignKey('garant.id'), primary_key=True, nullable=False)
    projet_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True, nullable=False)
    amount = db.Column(db.Float, default=0)


from app_racine.utils import PrintPDFView, PrintPDFResumeView
