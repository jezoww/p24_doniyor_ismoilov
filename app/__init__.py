from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['DATABASE_URI'] = 'db.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exam.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'top-secret-key'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

from app import routes
from app import models

