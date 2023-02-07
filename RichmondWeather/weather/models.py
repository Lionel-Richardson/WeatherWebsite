from weather import db

#SQL database model
class Weather(db.Model):
    __tablename__ = 'weather_site_temps'
    dataID = db.Column(db.Integer(), primary_key=True)
    source = db.Column(db.VARCHAR(length=50), nullable=True)
    temperature = db.Column(db.VARCHAR(length=50), nullable=True)
    conditions = db.Column(db.VARCHAR(length=50), nullable=True)
    time = db.Column(db.DATETIME(), nullable=True)