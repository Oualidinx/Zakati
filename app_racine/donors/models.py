from app_racine import db
from datetime import datetime
from app_racine.utilities import PaginationMixin


class DonateMosque(PaginationMixin, db.Model):
    __tablename__ = "donate_mosque"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    mosque_id = db.Column(db.Integer, db.ForeignKey('mosque.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    donor = db.relationship('User', primaryjoin="User.id == foreign(DonateMosque.user_id)", viewonly=True)
    mosque = db.relationship('Mosque', primaryjoin="Mosque.id==foreign(DonateMosque.mosque_id)", viewonly=True)

    def to_dict(self):
        return dict(
            id=self.id,
            date=str(self.created_at.date()),
            donor=self.donor.first_name + " " + self.donor.last_name,
            amount="{:,.2f}  ".format(self.amount) + "د.ج"
        )


class Participe(db.Model):
    __tablename__ = 'participe'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True, nullable=False)
