from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os 


templatedir = os.path.abspath("templates")

app = Flask(__name__, template_folder=templatedir)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'ufp.db') #ბასა კეთდება ამ მისამართზე 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from view import view