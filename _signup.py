from flask import Flask, Blueprint, redirect, render_template, request, session
from passlib.hash import sha256_crypt

from sqlalchemy import *


import _app
from _logout import *

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
		sesso = request.form['sesso']

		users = _app.User.query.all()
		for user in users:
			if user.username == username:
				err += 1
				alert = '* USERNAME GIÀ REGISTRATO *'
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
			passw = sha256_crypt.hash(passw)	
			new_user = _app.User(username, nome, cognome, email, passw, indirizzo, città, codice_fiscale, sesso, telefono, data_nascita)
			_app.db.session.add(new_user)
			_app.db.session.commit()

			return redirect('/')


	return render_template('signup.html', alert = alert, session=session)
	