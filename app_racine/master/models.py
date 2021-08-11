from app_racine import db
from app_racine.utilities import PaginationMixin


class Critere(PaginationMixin, db.Model):
    __tablename__ = "critere"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    label = db.Column(db.String(50), unique=True)
    category = db.Column(db.String(50))
    weight = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.label,
            category=self.category,
            weight=self.weight
        )


class Project(PaginationMixin, db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    Description = db.Column(db.Text)
    montant_estime = db.Column(db.Float, nullable=False, default=0.0)
    montant_quantise = db.Column(db.Float, default=0.0)

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            Description=self.Description,
            montant_estime=self.montant_estime,
            montant_quantise=self.montant_quantise
        )


class ParameterUtils(PaginationMixin, db.Model):
    __tablename__ = "parameter_utils"
    id = db.Column(db.Integer, primary_key=True)
    taux_scolaire = db.Column(db.Integer, default=0)
    taux_prime_m = db.Column(db.Integer, default=0)
    salaire_base = db.Column(db.Integer, default=20000)

    def to_dict(self):
        return dict(
            id=self.id,
            taux_scolaire=self.taux_scolaire,
            taux_prime_m=self.taux_prime_m,
            salaire_base=self.salaire_base
        )


class Wilaya(PaginationMixin, db.Model):
    __tablename__ = 'wilaya'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.Integer, default=0)
    mosques = db.relationship('Mosque', backref="mosques_wilayas", lazy="subquery")

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            zip_code=self.zip_code
        )
