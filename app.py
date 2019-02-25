from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://olzatrjzhhxuon:2cc542237dc6b08ee996a94181bc972144e0dce38b2b867c2140c2aecad3059b@ec2-54-204-41-109.compute-1.amazonaws.com/d6n7s0roossktr'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '$al3mr3!gn$FEB'

UPLOAD_FOLDER = './images/users/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

