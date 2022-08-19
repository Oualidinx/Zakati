from app_racine import database
from app_racine.utilities import PaginationMixin
from arabic_reshaper import reshape

class Critere(PaginationMixin, database.Model):
    __tablename__ = "critere"
    id = database.Column(database.Integer, primary_key=True, nullable=False)
    label = database.Column(database.String(50), unique=True)
    category = database.Column(database.String(50))
    weight = database.Column(database.Float, nullable=False)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.label,
            category=self.category,
            weight=self.weight
        )

    def __repr__(self):
        return reshape(f'{self.id},{self.label},{self.category},{self.weight}')


class Project(PaginationMixin, database.Model):
    __tablename__ = 'project'
    id = database.Column(database.Integer, primary_key=True, nullable=False)
    title = database.Column(database.String(50), nullable=False)
    Description = database.Column(database.Text)
    montant_estime = database.Column(database.Float, nullable=False, default=0.0)
    montant_quantise = database.Column(database.Float, default=0.0)

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            Description=self.Description,
            montant_estime=self.montant_estime,
            montant_quantise=self.montant_quantise
        )


class ParameterUtils(PaginationMixin, database.Model):
    __tablename__ = "parameter_utils"
    id = database.Column(database.Integer, primary_key=True)
    taux_scolaire = database.Column(database.Integer, default=0)
    taux_prime_m = database.Column(database.Integer, default=0)
    salaire_base = database.Column(database.Integer, default=20000)

    def to_dict(self):
        return dict(
            id=self.id,
            taux_scolaire=self.taux_scolaire,
            taux_prime_m=self.taux_prime_m,
            salaire_base=self.salaire_base
        )


class Wilaya(PaginationMixin, database.Model):
    __tablename__ = 'wilaya'
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(50), nullable=False)
    zip_code = database.Column(database.Integer, default=0)
    mosques = database.relationship('Mosque', backref="mosques_wilayas", lazy="subquery")

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            zip_code=self.zip_code
        )
