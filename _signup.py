from flask import Flask, Blueprint, redirect, render_template, request, session
from passlib.hash import sha256_crypt
from codicefiscale import codicefiscale
import time

from sqlalchemy import *

import _app
from _logout import *
from formattazione_data import *
from iban_generator import *

signup_bp = Blueprint('signup_bp', __name__)

@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
	logout()
	alert = ""
	if request.method == 'POST':
		err = 0
		nome = request.form['nome']
		cognome = request.form['cognome']
		username = request.form['username']
		email = request.form['email']
		passw = request.form['passw']
		confirm_passw = request.form['confirm_passw']
		codice_fiscale = request.form['codice_fiscale']
		indirizzo = request.form['indirizzo']
		città = request.form['città']
		telefono = request.form['telefono']
		data_nascita = request.form['data_nascita']
		città_nascita = request.form['città_nascita']
		sesso = request.form['sesso']

		data_nascita_formattata = formatta_data(data_nascita)

		users = _app.User.query.all()
		for user in users:
			if user.username == username:
				err += 1
				alert = '* USERNAME GIÀ REGISTRATO *'
			elif codicefiscale.encode(surname = cognome, name = nome, sex = sesso, birthdate = data_nascita_formattata, birthplace = città_nascita) != codice_fiscale:
				err += 1
				alert = '* CODICE FISCALE ERRATO *'
			elif user.email == email:
				err += 1
				alert = '* EMAIL GIÀ REGISTRATA *'
			elif passw != confirm_passw:
				err += 1
				alert = '* LE PASSWORD NON CORRISPONDONO *'
			elif (len(passw) < 8 or any(map(str.isdigit, passw)) == False):
				err += 1
				alert = '* ALMENO 8 CARATTERI E 1 NUMERO *'
			elif user.codice_fiscale == codice_fiscale:
				err += 1
				alert = '* CODICE FISCALE GIÀ REGISTRATO *'



		if err == 0:
			session['logged_in'] = True
			session['username'] = username
			passw = sha256_crypt.hash(passw)	
			iban = generate_iban()

			new_user = _app.User(username, nome, cognome, email, passw, indirizzo, città, codice_fiscale, sesso, telefono, data_nascita, città_nascita)
			_app.db.session.add(new_user)
			_app.db.session.commit()
			_app.db.session.refresh(new_user)
			
	
			new_conto = _app.Conto(iban, new_user.id_user)
			_app.db.session.add(new_conto)
			_app.db.session.commit()
			_app.db.session.refresh(new_conto)


			saldo = _app.Saldo(0, 0, new_conto.id_conto)
			_app.db.session.add(saldo)	
			
			_app.db.session.commit()

			time.sleep(2.5)

			return redirect('/redirecting')


	return render_template('signup.html', alert = alert, session=session)
	