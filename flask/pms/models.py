from pms import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from simplecrypt import encrypt, decrypt
from base64 import b64encode, b64decode

class Users(UserMixin, db.Model):
    """
    Create users table
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, unique=True)
    pw_hash = db.Column(db.String(255))
    pw_expire_date = db.Column(db.DateTime(timezone=True), default=func.now())

    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttibuteError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.pw_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=32)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.pw_hash, password)
    def get_expire_date(self):
        """
        Return expire date of the password
        """
        return self.pw_expire_date

    def __repr__(self):
        return '<Username: {}'.format(self.username)


class Services(UserMixin, db.Model):
    """
    Create service table
    """
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    service_name = db.Column(db.String(255), index=True)
    encrypted_pw = db.Column(db.String(255), index=True)
    username = db.Column(db.String(255), index=True)





# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
