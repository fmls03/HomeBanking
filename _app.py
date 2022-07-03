from enum import unique
from flask import Flask, redirect
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

from _login import *    
from _home import *
from _logout import *
from _redirecting import *
from _signup import *
from _bonifico_istantaneo import *
from _admin import *

secret_key = str(os.urandom(256))

app = Flask(__name__)
app.config['SECRET_KEY']= secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://fmls03:Schipilliti03@localhost/HomeBanking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "100"))
WEB_CONCURRENCY = int(os.getenv("WEB_CONCURRENCY", "2"))
POOL_SIZE = max(DB_POOL_SIZE // WEB_CONCURRENCY, 5)

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = dict(pool_size=POOL_SIZE, max_overflow=0)

db = SQLAlchemy(app)


app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(redirecting_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(bonifico_bp)
app.register_blueprint(admin_bp)


class User(db.Model):
    __tablename__ = 'user'
    id_user = db.Column(db.Integer, autoincrement=True, primary_key = True)
    username = db.Column(db.VARCHAR(255), unique=True)
    nome = db.Column(db.VARCHAR(255))
    cognome = db.Column(db.VARCHAR(255))
    email = db.Column(db.VARCHAR(255))
    passw = db.Column(db.VARCHAR(255))
    indirizzo = db.Column(db.VARCHAR(255))
    città = db.Column(db.VARCHAR(255))
    codice_fiscale = db.Column(db.String(16), unique=True)
    sesso = db.Column(db.String(1))
    telefono = db.Column(db.VARCHAR(12))
    data_nascita = db.Column(db.Date)
    città_nascita = db.Column(db.VARCHAR(255))

    conto = db.relationship('Conto', backref='user', uselist=False)

    def __init__(self, username, nome, cognome, email, passw, indirizzo, città, codice_fiscale, sesso, telefono, data_nascita, città_nascita):
        self.username = username
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.passw = passw
        self.indirizzo = indirizzo
        self.città = città
        self.codice_fiscale = codice_fiscale
        self.sesso = sesso
        self.telefono = telefono
        self.data_nascita = data_nascita
        self.città_nascita = città_nascita


class Conto(db.Model):
    __tablename__ = 'conto'
    id_conto = db.Column(db.Integer, autoincrement=True, primary_key=True)
    iban = db.Column(db.VARCHAR(27),unique=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'))

    saldo = db.relationship('Saldo', backref='conto', uselist=False) 
    transazioni = db.relationship('Transazione', backref='conto') 


    def __init__(self, iban, id_user):
        self.iban = iban
        self.id_user = id_user


class Saldo(db.Model):
    __tablename__ = 'saldo'
    id_saldo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    saldo_contabile = db.Column(db.Float)
    saldo_disponibile = db.Column(db.Float)
    id_conto = db.Column(db.Integer, db.ForeignKey('conto.id_conto'), unique=True)

    def __init__(self, saldo_contabile, saldo_disponibile, id_conto):
        self.saldo_contabile = saldo_contabile
        self.saldo_disponibile  = saldo_disponibile
        self.id_conto = id_conto
        

class Transazione(db.Model):
    __tablename__ = 'transazione'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_mittente = db.Column(db.VARCHAR(255))
    iban_destinatario = db.Column(db.CHAR(27))
    importo = db.Column(db.Float)
    data = db.Column(db.DateTime)
    causale = db.Column(db.VARCHAR(255))
    id_conto = db.Column(db.Integer, db.ForeignKey('conto.id_conto'))

    def __init__(self, user_mittente, iban_destinatario, importo, data, causale, id_conto):
        self.user_mittente = user_mittente
        self.iban_destinatario = iban_destinatario
        self.importo = importo
        self.data = data
        self.causale = causale
        self.id_conto = id_conto

@app.route('/')
def index():
    return redirect('/logout')

if __name__ == '__main__':
    app.run('localhost', 5000, debug=True, threaded=True) 
