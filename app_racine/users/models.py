from app_racine import database, app, login
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedSerializer as Serializer


class User(database.Model, UserMixin):
    __tablename__ = 'user'
    id = database.Column(database.Integer, primary_key=True, nullable=False)
    username = database.Column(database.String(50), nullable=False)
    first_name = database.Column(database.String(50), nullable=False)
    last_name = database.Column(database.String(50), nullable=False)
    phone_number = database.Column(database.String(10), nullable=False, index=True)
    email = database.Column(database.String(100))
    address = database.Column(database.String(255))
    password = database.Column(database.String(512), nullable=False)
    mosques = database.relationship('Mosque', secondary="donate_mosque",
                                    primaryjoin='User.id == foreign(DonateMosque.user_id)',
                                    secondaryjoin="Mosque.id == foreign(DonateMosque.id)", viewonly=True
                                    )
    create_at = database.Column(database.DateTime, default=datetime.utcnow())
    role = database.Column(database.String(50))

    def __repr__(self):
        return super().__repr__()

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email
        }

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
