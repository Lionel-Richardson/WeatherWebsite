from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:python@localhost/weather'
app.config['SECRET_KEY'] = 'my secret key'
db = SQLAlchemy(app)

from weather import routes