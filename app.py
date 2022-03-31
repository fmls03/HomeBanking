from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

from home import *

secret_key = str(os.urandom(256))

app = Flask(__name__)
app.config['SECRET_KEY']= secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://fmlspi:Schipilliti03!@93.51.26.126/HomeBanking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

app.register_blueprint(home_bp)


class User(db.Model):
    id_user = db.Column(db.Integer, auto_increment=True, primary key = True)
    username = db.Column(db.VARCHAR(255))
    nome = db.Column(db.VARCHAR(255))
    cognome = db.Column(db.VARCHAR(255))
    indirizzo = db.Column(db.VARCHAR(255))
    città = db.Column(db.VARCHAR(255))
    codice_fiscale = db.Column(db.String(16))
    sesso = db.Column(db.String(1))
    telefono = db.Column(db.VARCHAR(12))
    data_nascita = db.Column(db.Date)
    mail = db.Column(db.VARCHAR(255))
    

if __name__ == '__main__':
    app.run('localhost', 5000, debug=True)