from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://christina:r3!gn$AL3M@localhost/shhh_auction'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)