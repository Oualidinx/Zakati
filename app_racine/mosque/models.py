from app_racine import database
from datetime import datetime
from app_racine.utilities import PaginationMixin


class Garant(PaginationMixin, database.Model):
    __tablename__ = "garant"
    id = database.Column(database.Integer, primary_key=True, nullable=False)  # le compte ccp
    ccp = database.Column(database.String(20), nullable=False)
    id_card_num = database.Column(database.String(100), nullable=False)
    id_card_release_date = database.Column(database.Date, nullable=False)
    id_card_release_authority = database.Column(database.String(256), nullable=False)
    cle_CCP = database.Column(database.Integer, nullable=False)
    nom = database.Column(database.String(50), nullable=False)
    prenom = database.Column(database.String(50), nullable=False)
    address = database.Column(database.String(100), nullable=False)
    # cronic_deseases = database.Column(database.JSON, nullable=True)
    phone_number = database.Column(database.String(10), nullable=False)
    created_at = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    date_nais = database.Column(database.DateTime, nullable=False)
    num_extrait_nais = database.Column(database.Integer, nullable=False)
    Solde_finale = database.Column(database.Float, default=0)  # عدد الاسهــم
    Solde_points = database.Column(database.Integer, default=0)  # رصيد النقاط
    Solde_part_financiere = database.Column(database.Float, default=0)  # المبلغ المستحق للمحتاج
    is_active = database.Column(database.SmallInteger, default=1)
    familly = database.relationship('Personne', backref="person", lazy=True)
    mosque_id = database.Column(database.Integer, database.ForeignKey('mosque.id'), nullable=False)
    prime_mensuelle = database.Column(database.Float, default=0)
    prime_scolaire = database.Column(database.Float, default=0)
    work = database.relationship('Critere', secondary="situation_garant", viewonly=True,
                                 primaryjoin="remote(SituationGarant.garant_id) == Garant.id",
                                 secondaryjoin="and_(remote(Critere.id) == SituationGarant.critere_id,"
                                               "Critere.label=='بطال')"
                                 )

    salary = database.relationship('Critere', secondary="situation_garant", viewonly=True,
                                   primaryjoin="remote(SituationGarant.garant_id) == Garant.id",
                                   secondaryjoin="and_(remote(Critere.id) == SituationGarant.critere_id,"
                                                 "Critere.label=='أجر تحت الأجر القاعدي')"
                                   )
    decript = database.relationship('Critere', viewonly=True, secondary="critere",
                                    primaryjoin="remote(SituationGarant.garant_id) == Garant.id",
                                    secondaryjoin="and_(remote(Critere.id) == SituationGarant.critere_id,"
                                                  "Critere.label=='عاجز')"
                                    )
    sick = database.relationship('Critere', viewonly=True, secondary="situation_garant",
                                 primaryjoin="remote(SituationGarant.garant_id) == Garant.id",
                                 secondaryjoin="and_(remote(Critere.id) == SituationGarant.critere_id,"
                                               "Critere.label =='مرض مزمن')")
    residence_ownership = database.relationship('Critere', viewonly=True, secondary="situation_garant",
                                                primaryjoin="remote(SituationGarant.garant_id) == Garant.id",
                                                secondaryjoin="and_(remote(Critere.id) == SituationGarant.critere_id,"
                                                              "or_(Critere.label=='سكن بتأجير', Critere.label == 'سكن "
                                                              "في دار العائلة' "
                                                              "))"
                                                )
    residence_validity = database.relationship('Critere', viewonly=True, secondary="situation_garant",
                                               primaryjoin="remote(SituationGarant.garant_id) == Garant.id",
                                               secondaryjoin="and_(remote(Critere.id) == SituationGarant.critere_id,"
                                                             "Critere.label=='سكن غير صالح')")
    health_assurance = database.relationship('Critere', viewonly=True, secondary="situation_garant",
                                             primaryjoin="remote(SituationGarant.garant_id) == Garant.id",
                                             secondaryjoin="and_(remote(Critere.id) == SituationGarant.critere_id,"
                                                           "Critere.label=='غير مؤمن')")
    electrical_appliances = database.relationship('Critere', viewonly=True, secondary="situation_garant",
                                                  primaryjoin="remote(SituationGarant.garant_id) == Garant.id",
                                                  secondaryjoin="and_(remote(Critere.id) == SituationGarant.critere_id,"
                                                                "Critere.category=='الاجهزة الكهرومنزلية')")
    """def print_form(self):  # return a response token
        return print_PDF_view(self.id)"""

    def print_form(self):  # return a response token
        return PrintPDFView(self.id)

    def get_total_sum(self):
        self.Solde_part_financiere = self.Solde_finale * Mosque.get_value()
        database.session.add(self)
        database.session.commit()
        return self.Solde_part_financiere

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.nom,
            last_name=self.prenom,
            solde_finale=self.get_total_sum(),
            date_nais=self.date_nais.date(),
            status=self.is_active
        )

    def data(self):
        return dict(
            id=self.id,
            name=self.nom,
            last_name=self.prenom,
            phone_number=self.phone_number,
            date_nais=self.date_nais.date(),
            id_card_number=self.id_card_num,
            id_card_release_date=self.id_card_release_date,
            id_card_release_authority=self.id_card_release_authority,
            address=self.address,
            ccp=self.ccp,
            salary=self.salary if self.salary or len(self.salary) != 0 else None,
            decrepit=self.decript if self.decript or len(self.decript) != 0 else None,
            work=self.work if self.work or len(self.work) != 0 else None,
            sick=self.sick if self.sick or len(self.sick) != 0 else None,
            residence_ownership=self.residence_ownership if self.residence_ownership or len(
                self.residence_ownership) != 0 else None,
            residence_validity=self.residence_validity if self.residence_validity or len(
                self.residence_validity) != 0 else None,
            health_assurance=self.health_assurance if self.health_assurance or len(
                self.health_assurance) != 0 else None,
            familly=[
                person.to_dict() for person in Personne.query.filter_by(garant_id=self.id).all()
            ],
            electrical_appliances=[t.label for t in self.electrical_appliances],
            cle_ccp=self.cle_CCP,
            arrows=self.Solde_finale,
            status=self.is_active
        )


class Mosque(PaginationMixin, database.Model):
    __tablename__ = "mosque"
    id = database.Column(database.Integer, primary_key=True, nullable=False)
    nom = database.Column(database.String(50), nullable=False)
    inscrits = database.relationship('Garant', backref='beneficaire', lazy='subquery')
    addresse = database.Column(database.String(100), nullable=False)
    country = database.Column(database.String(50), nullable=False, default="الجزائر")
    num_tele = database.Column(database.String(10), nullable=False)
    # email = db.Column(db.String(100))
    user_account = database.Column(database.Integer, database.ForeignKey('user.id'))
    category = database.Column(database.String(6), nullable=False)
    state = database.Column(database.Integer, database.ForeignKey('wilaya.id'))
    username = database.relationship('User', primaryjoin="User.id == foreign(Mosque.user_account)", viewonly=True)
    donors = database.relationship('DonateMosque', backref="collected_amount", lazy="subquery")

    @staticmethod
    def PrintResume(project_id):
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
        # print(Garant.query.first().Solde_points)
        if Garant.query.filter_by(is_active=1).first():
            print(Garant.query.filter_by(is_active=1).order_by(Garant.Solde_points.asc()).first().to_dict())
            min_points = Garant.query.filter_by(is_active=1).order_by(Garant.Solde_points.asc()).first().Solde_points
        if min_points != 0:
            g_list = Garant.query.filter_by(is_active=1).all()
            for person in g_list:
                person.Solde_finale = round(person.Solde_points / min_points, 2)
                database.session.add(person)
                database.session.commit()

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


class SituationGarant(PaginationMixin, database.Model):
    __tablename__ = "situation_garant"
    garant_id = database.Column(database.Integer, database.ForeignKey('garant.id'), primary_key=True, nullable=False)
    critere_id = database.Column(database.Integer, database.ForeignKey('critere.id'), primary_key=True)


class SituationPerson(PaginationMixin, database.Model):
    __tablename__ = "situation_person"
    personne_id = database.Column(database.Integer, database.ForeignKey('personne.id'), primary_key=True)
    critere_id = database.Column(database.Integer, database.ForeignKey('critere.id'), primary_key=True)


class Personne(PaginationMixin, database.Model):
    __tablename__ = "personne"
    id = database.Column(database.Integer, primary_key=True, nullable=False)
    nom = database.Column(database.String(50), nullable=False)
    prenom = database.Column(database.String(50), nullable=False)
    # cronic_desease = database.Column(database.String(100), nullable=True)
    date_naissance = database.Column(database.DateTime, nullable=False)
    relation_ship = database.Column(database.String(6), nullable=False, default="")
    garant_id = database.Column(database.Integer, database.ForeignKey('garant.id'), nullable=False)  # le compte ccp
    situation = database.relationship('Critere', secondary='situation_person', viewonly=True,
                                      primaryjoin='remote(SituationPerson.personne_id) == Personne.id',
                                      secondaryjoin ='remote(Critere.id)==SituationPerson.critere_id'
                                      )
    work = database.relationship('Critere', secondary="situation_person", viewonly=True,
                                 primaryjoin="remote(SituationPerson.personne_id) == Personne.id",
                                 secondaryjoin="and_(remote(Critere.id) == SituationPerson.critere_id, "
                                               "Critere.label=='بطال')"
                                 )

    salary = database.relationship('Critere', secondary="situation_person", viewonly=True,
                                   primaryjoin="remote(SituationPerson.personne_id) == Personne.id",
                                   secondaryjoin="and_(remote(Critere.id) == SituationPerson.critere_id, "
                                                 "Critere.label=='أجر تحت الأجر القاعدي' )"
                                   )
    decript = database.relationship('Critere', secondary="situation_person", viewonly=True,
                                    primaryjoin="remote(SituationPerson.personne_id) == Personne.id",
                                    secondaryjoin="and_(remote(Critere.id) == SituationPerson.critere_id, "
                                                  "Critere.label=='عاجز')"
                                    )
    sick = database.relationship('Critere', secondary="situation_person", viewonly=True,
                                 primaryjoin="remote(SituationPerson.personne_id) == Personne.id",
                                 secondaryjoin="and_(remote(Critere.id) == SituationPerson.critere_id, "
                                               "Critere.label =='مرض مزمن')")
    orphan = database.relationship('Critere', secondary="situation_person", viewonly=True,
                                   primaryjoin="remote(SituationPerson.personne_id) == Personne.id",
                                   secondaryjoin="and_(remote(Critere.id) == SituationPerson.critere_id, "
                                                 "Critere.label =='يتيم(ة)')")

    study = database.relationship('Critere', secondary="situation_person", viewonly=True,
                                  primaryjoin="remote(SituationPerson.personne_id) == Personne.id",
                                  secondaryjoin="and_(remote(Critere.id) == SituationPerson.critere_id, "
                                                "Critere.label =='متمدرس(ة)')")

    divorce = database.relationship('Critere', secondary="situation_person", viewonly=True,
                                    primaryjoin="remote(SituationPerson.personne_id) == Personne.id",
                                    secondaryjoin="and_(remote(Critere.id) == SituationPerson.critere_id, "
                                                  "Critere.label =='مطلق(ة)')")

    single = database.relationship('Critere', secondary="situation_person", viewonly=True,
                                   primaryjoin="remote(SituationPerson.personne_id) == Personne.id",
                                   secondaryjoin="and_(remote(Critere.id) == SituationPerson.critere_id, "
                                                 "Critere.label =='عزباء')")

    widow = database.relationship('Critere', secondary="situation_person", viewonly=True,
                                  primaryjoin="remote(SituationPerson.personne_id) == Personne.id",
                                  secondaryjoin="and_(remote(Critere.id) == SituationPerson.critere_id, "
                                                "Critere.label =='أرمل(ة)')")

    complicated = database.relationship('Critere', secondary="situation_person", viewonly=True,
                                        primaryjoin="remote(SituationPerson.personne_id) == Personne.id",
                                        secondaryjoin="and_(remote(Critere.id) == SituationPerson.critere_id, "
                                                      "Critere.label =='معلقة')")

    def to_dict(self):
        return dict(
            first_name=self.nom,
            last_name=self.prenom,
            date_naissance=self.date_naissance.date(),
            relation_ship=self.relation_ship,
            situation = [int(x.id) for x in self.situation],
            decrepit=self.decript if self.decript or len(self.decript) != 0 else None,
            work=self.work if self.work or len(self.work) != 0 else None,
            sick=self.sick if self.sick or len(self.sick) != 0 else None,
            orphan=self.orphan if self.orphan or len(self.orphan) != 0 else None,
            study=self.study if self.study or len(self.study) != 0 else None,
            divorce=self.divorce if self.divorce or len(self.divorce) != 0 else None,
            single=self.single if self.single or len(self.single) != 0 else None,
            widow=self.widow if self.widow or len(self.widow) != 0 else None,
            complicated=self.complicated
        )


class GarantProject(PaginationMixin, database.Model):
    garant_id = database.Column(database.Integer, database.ForeignKey('garant.id'), primary_key=True, nullable=False)
    projet_id = database.Column(database.Integer, database.ForeignKey('project.id'), primary_key=True, nullable=False)
    amount = database.Column(database.Float, default=0)


from app_racine.utils import PrintPDFView, PrintPDFResumeView
