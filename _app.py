from flask import Flask, session, Blueprint
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

from _home import *
from _login import *    
from _logout import *
from _redirecting import *

secret_key = str(os.urandom(256))

app = Flask(__name__)
app.config['SECRET_KEY']= secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://fmlspi:Schipilliti03!@93.51.26.126/HomeBanking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(redirecting_bp)


class User(db.Model):
    __tablename__ = 'user'
    id_user = db.Column(db.Integer, auto_increment=True, primary_key = True)
    username = db.Column(db.VARCHAR(255))
    nome = db.Column(db.VARCHAR(255))
    cognome = db.Column(db.VARCHAR(255))
    mail = db.Column(db.VARCHAR(255))
    passw = db.Column(db.VARCHAR(255))
    indirizzo = db.Column(db.VARCHAR(255))
    città = db.Column(db.VARCHAR(255))
    codice_fiscale = db.Column(db.String(16))
    sesso = db.Column(db.String(1))
    telefono = db.Column(db.VARCHAR(12))
    data_nascita = db.Column(db.Date)

    conto = db.relationship('Conto', backref=('user'))

    def __init__(self, username, nome, cognome, mail, passw, indirizzo, città, codice_fiscale, sesso, telefono, data_nascita):
        self.username = username
        self.nome = nome
        self.cognome = cognome
        self.mail = mail
        self.passw = passw
        self.indirizzo = indirizzo
        self.città = città
        self.codice_fiscale = codice_fiscale
        self.sesso = sesso
        self.telefono = telefono
        self.data_nascita = data_nascita
  

class Conto(db.Model):
    __tablename__ = 'conto'
    id = db.Column(db.Integer, auto_increment=True)
    iban = db.Column(db.VARCHAR(27))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'))
    n_conto = db.Column(db.VARCHAR(27), primary_key=True)

    saldo = db.relationship('Saldo', backref=('conto')) 
    transazione = db.relationship('Transazione', backref=('conto')) 


    def __init__(self, iban, id_user, n_conto):
        self.iban = iban
        self.id_user = id_user
        self.n_conto = n_conto


class Saldo(db.Model):
    __tablename__ = 'saldo'
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    importo = db.Column(db.Float)
    n_conto = db.Column(db.VARCHAR(27), db.ForeignKey('conto.n_conto'))

    def __init__(self, importo, n_conto):
        self.importo = importo
        self.n_conto = n_conto
        

class Transazione(db.Model):
    __tablename__ = 'transazione'
    id = db.Column(db.Integer, auto_increment=True, primary_key=True)
    iban2 = db.Column(db.VARCHAR(27))
    importo = db.Column(db.Float)
    data = db.Column(db.Date)
    descrizione = db.Column(db.VARCHAR(255))
    n_conto = db.Column(db.VARCHAR(27), db.ForeignKey('conto.n_conto'))

    def __init__(self, iban2, importo, data, n_conto):
        self.iban2 = iban2
        self.importo = importo
        self.data = data
        self.n_conto = n_conto


@app.route('/')
def clear_all():
    session.clear()
    return redirect('/redirecting')


if __name__ == '__main__':
    app.run('localhost', 5000, debug=True)  
    clear_all()