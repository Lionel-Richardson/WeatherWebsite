from weather import db, login_manager
from weather import bcrypt
from flask_login import UserMixin

#needed to create an instance of the user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#SQL database user model with hashed password
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


#SQL database weather model
class Weather(db.Model):
    __tablename__ = 'weather_site_temps'
    dataID = db.Column(db.Integer(), primary_key=True)
    source = db.Column(db.VARCHAR(length=50), nullable=True)
    temperature = db.Column(db.VARCHAR(length=50), nullable=True)
    conditions = db.Column(db.VARCHAR(length=50), nullable=True)
    time = db.Column(db.DATETIME(), nullable=True)