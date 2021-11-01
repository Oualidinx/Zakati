from app_racine import db, app, login
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False, index=True)
    email = db.Column(db.String(100))
    address = db.Column(db.String(255))
    password = db.Column(db.String(512), nullable=False)
    mosques = db.relationship('Mosque', secondary="donate_mosque",
                              primaryjoin='User.id == foreign(DonateMosque.user_id)',
                              secondaryjoin="Mosque.id == foreign(DonateMosque.id)", viewonly=True
                              )
    create_at = db.Column(db.DateTime, default=datetime.utcnow())
    role = db.Column(db.String(50))

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
