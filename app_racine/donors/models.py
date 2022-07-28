from app_racine import database
from datetime import datetime
from app_racine.utilities import PaginationMixin


class DonateMosque(PaginationMixin, database.Model):
    __tablename__ = "donate_mosque"
    id = database.Column(database.Integer, primary_key=True, nullable=False)
    mosque_id = database.Column(database.Integer, database.ForeignKey('mosque.id'), nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    amount = database.Column(database.Float, default=0.0)
    created_at = database.Column(database.DateTime, default=datetime.utcnow())
    donor = database.relationship('User', primaryjoin="User.id == foreign(DonateMosque.user_id)", viewonly=True)
    mosque = database.relationship('Mosque', primaryjoin="Mosque.id==foreign(DonateMosque.mosque_id)", viewonly=True)

    def to_dict(self):
        return dict(
            id=self.id,
            date=str(self.created_at.date()),
            donor=self.donor.first_name + " " + self.donor.last_name,
            amount="{:,.2f}  ".format(self.amount) + "د.ج"
        )


class Participe(database.Model):
    __tablename__ = 'participe'
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), primary_key=True, nullable=False)
    project_id = database.Column(database.Integer, database.ForeignKey('project.id'), primary_key=True, nullable=False)
